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
from enums import ErrorCode
from errors import ApiError
from hardware_controller import HardwareController
from helpers import (
    cleanup_gpio,
    configure_logging,
    configure_status_led,
    json_dumps,
    load_config,
    turn_led_indicator_off,
    turn_led_indicator_on,
)
from responses import ResponseError

# TODO: update all command documentation (new "command" field for all responses)
# TODO: update all command documentation (all commands should have "payload" and inside is the content, also errors)
# TODO: TEST all commands (turn_off DONE, turn_on DONE, status PENDING)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: avoid leaving inactive connections when Home assistant fails to send a command a need to establish a new connection

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

    async def handler(request: Request) -> None:

        ws = WebSocketResponse()
        await ws.prepare(request)
        LOGGER.info(
            "New client connected from %s",
            request.get_extra_info("peername", request.remote),
        )
        LOGGER.info("Ready to receive commands from client")

        parser = CommandParser(hw_controller)

        async for msg in ws:

            if msg.type != aiohttp.WSMsgType.TEXT:
                LOGGER.error(
                    "Message received with an invalid WebSocket message type: %s",
                    msg.type.name,
                )
                response = ResponseError(
                    HTTPStatus.BAD_REQUEST,
                    {
                        "code": ErrorCode.BAD_REQUEST,
                        "description": f"Message type {msg.type.name}"
                        "not valid for commands, use TEXT",
                    },
                )
            else:
                try:
                    cmd = parser.parse(msg.data)

                    LOGGER.debug("Command received : %s", msg.json())

                    # TODO: validation should be done internally in parser.parse
                    cmd.validate_arguments()
                    response = cmd.run()

                except ApiError as e:
                    response = ResponseError(e.status, {"code": e.code })

                    LOGGER.debug("", exc_info=e)
                except Exception:
                    response = ResponseError(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        {"code": ErrorCode.INTERNAL_ERROR},
                    )

                    LOGGER.exception("Exception")

            response_as_string = json_dumps(response)
            await ws.send_json(response_as_string)

            if isinstance(cmd, Disconnect):
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
