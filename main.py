"""Starts the application."""

import logging
import sys
from http import HTTPStatus
from typing import Callable, Coroutine

import aiohttp
from aiohttp.web import Application, Request, WebSocketResponse, get, run_app
from scapy.all import ICMP, IP, sr1

sys.path.append("./src")

from commands.disconnect import Disconnect
from controllers import HardwareController
from enums import ErrorCode
from errors import ApiError
from models.internal.config import Config
from models.responses import Error, ResponseError
from utils import Collector, to_dict
from utils.commands import CommandParser
from utils.config import configure_logging, configure_status_led, load_configurations
from utils.gpio import cleanup_gpio_ports, turn_led_off, turn_led_on

# TODO: TEST all commands (turn_off DONE, turn_on DONE, status PENDING)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: fix disconnect

LOGGER = logging.getLogger(__name__)

def build_app_handler(
    command_parser: CommandParser,
) -> Callable[[Request], Coroutine[None, None, None]]:
    """Build the app handler (coroutine) to handle incoming messages.

    Args:
        command_parser (CommandParser): Command parser.

    Returns:
        CoroutineType[Any, Any, None]: Returns the coroutine

    """
    async def handler(request: Request) -> None:

        ws = WebSocketResponse()
        await ws.prepare(request)
        client = request.get_extra_info("peername", request.remote)
        collector.add_client(client)

        LOGGER.info("New client connected from %s", client)

        async for msg in ws:

            error = None
            cmd = None

            if msg.type != aiohttp.WSMsgType.TEXT:
                LOGGER.error(
                    "Message received with an invalid WebSocket message type: %s",
                    msg.type.name,
                )

                error = Error(
                    code=ErrorCode.BAD_REQUEST,
                    description=f"Message type {msg.type.name} not valid, use TEXT",
                )
                response = ResponseError(HTTPStatus.BAD_REQUEST, error)
            else:
                try:
                    cmd = command_parser.parse(msg.data)

                    LOGGER.debug("Command received : %s", msg.json())

                    cmd.validate_arguments()
                    response = cmd.run()

                except ApiError as e:
                    error = Error(
                        e.code,
                        e.message if e.message is not None else "Internal server error",
                    )
                    response = ResponseError(e.status, error)

                    LOGGER.debug("", exc_info=e)
                except Exception:
                    error = Error(
                        ErrorCode.INTERNAL_SERVER_ERROR, "Internal server error"
                    )
                    response = ResponseError(HTTPStatus.INTERNAL_SERVER_ERROR, error)

                    LOGGER.exception("Exception")

            response.command = cmd.command_name if cmd is not None else "unknown"
            response_as_dict = to_dict(response)
            await ws.send_json(response_as_dict)

            if not error and isinstance(cmd, Disconnect):
                await ws.close()
                break

        collector.remove_client(client)

    return handler


def validate_icmp_reply(config: Config, icmp_reply) -> None:
     """Validate the result of `sr1` function from `scapy.all`."""
     if icmp_reply is None:
        raise ApiError(message=f"No answer from {config.default_gateway}")

if __name__ == "__main__":
    config = load_configurations()
    configure_logging(config)
    configure_status_led(config)

    """Using the controller to handle the strip is thread-safe under the assumption that
    there's  only one thread managing the event loop.
    """
    hw_controller = HardwareController(config)
    collector = Collector()
    command_parser = CommandParser(config, hw_controller, collector)
    exit_code = 0

    try:
        turn_led_off(config.status_led)
        reply = sr1(
            IP(dst=config.default_gateway) / ICMP(),
            iface=config.default_network_interface,
            timeout=config.connection_timeout,
            verbose=False,
        )
        validate_icmp_reply(config, reply)
        turn_led_on(config.status_led)

        app = Application()
        app.add_routes([get("/", build_app_handler(command_parser))])
        run_app(app, print=LOGGER.info)

    except Exception as ex:
        LOGGER.exception("", exc_info=ex)
        exit_code = 1
    finally:
        LOGGER.info("Finalizing server")
        cleanup_gpio_ports()
        sys.exit(exit_code)
