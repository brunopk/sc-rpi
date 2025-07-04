"""Entry point for the whole application."""

import logging
import sys
from http import HTTPStatus
from typing import Callable, Coroutine

import aiohttp
from aiohttp.web import Application, Request, WebSocketResponse, get, run_app
from scapy.all import ICMP, IP, sr1

sys.path.append("./src")

from command_parser import CommandParser
from commands.disconnect import Disconnect
from controllers import HardwareController
from enums import ErrorCode
from errors import ApiError
from helpers import (
    cleanup_gpio,
    configure_logging,
    configure_status_led,
    load_config,
    to_dict,
    turn_led_indicator_off,
    turn_led_indicator_on,
)
from models.responses import Error, ResponseError

# TODO: TEST all commands (turn_off DONE, turn_on DONE, status PENDING)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py

LOGGER = logging.getLogger(__name__)

def build_app_handler(
    hw_controller: HardwareController,
) -> Callable[[Request], Coroutine[None, None, None]]:
    """Build the app handler (coroutine) to handle incoming messages.

    Args:
        hw_controller (HardwareController): Used to control the strip

    Returns:
        CoroutineType[Any, Any, None]: Returns the coroutine

    """
    parser = CommandParser(hw_controller)

    async def handler(request: Request) -> None:

        ws = WebSocketResponse()
        await ws.prepare(request)

        LOGGER.info(
            "New client connected from %s",
            request.get_extra_info("peername", request.remote),
        )
        LOGGER.info("Ready to receive commands from client")

        async for msg in ws:

            error = None
            cmd_name = None

            if msg.type != aiohttp.WSMsgType.TEXT:
                LOGGER.error(
                    "Message received with an invalid WebSocket message type: %s",
                    msg.type.name,
                )

                error = Error(
                    code=ErrorCode.BAD_REQUEST,
                    description=f"Message type {msg.type.name} not valid for commands, "
                    "use TEXT",
                )
                response = ResponseError(HTTPStatus.BAD_REQUEST, error)
            else:
                try:
                    cmd = parser.parse(msg.data)
                    cmd_name = cmd.command_name

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

            response.command = cmd_name
            response_as_dict = to_dict(response)
            await ws.send_json(response_as_dict)

            if not error and isinstance(cmd, Disconnect):
                await ws.close()

    return handler


if __name__ == "__main__":
    config = load_config()
    host = config["DEFAULT"].get("host", "0.0.0.0")
    port = int(config["DEFAULT"].get("port", str(8080)))
    default_gateway = config["CONNECTION_CHECK"].get("default_gateway")
    iface = config["CONNECTION_CHECK"].get("iface")
    timeout = float(config["CONNECTION_CHECK"].get("timeout"))
    status_led = int(config["CONNECTION_CHECK"].get("status_led"))

    configure_logging(config)
    configure_status_led(config)

    # Using the controller to handle the strip is thread-safe under the assumption that there's only 
    # one thread managing the event loop.
    hw_controller = HardwareController(config)
    exit_code = 0
    logger = logging.getLogger("main")

    try:
        turn_led_indicator_off(status_led)
        reply = sr1(
            IP(dst=default_gateway) / ICMP(),
            iface=iface,
            timeout=timeout,
            verbose=False,
        )
        if reply is None:
            raise Exception("No answer from %s", default_gateway)
        turn_led_indicator_on(status_led)

        app = Application()
        app.add_routes([get("/", build_app_handler(hw_controller))])
        run_app(app, print=logger.info)

    except Exception as ex:
        LOGGER.exception("", exc_info=ex)
        exit_code = 1
    finally:
        LOGGER.info("Finalizing server")
        cleanup_gpio()
        sys.exit(exit_code)
