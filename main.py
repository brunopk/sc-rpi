#!/usr/bin/env python
import sys
import logging

from dataclasses import asdict
from http import HTTPStatus
from scapy.all import IP, ICMP, sr1
from aiohttp.web import Request, WebSocketResponse, Application, get, run_app

import aiohttp
import aiohttp.web 

sys.path.append('./src')

from response import Response, Error
from errors import ApiError
from commands import CommandParser
from commands.disconnect import Disconnect
from controller import Controller
from helpers import configure_logging, configure_status_led, load_config, turn_led_indicator_on, turn_led_indicator_off, cleanup_gpio


# TODO: TEST all commands (turn_off DONE, turn_on DONE, status PENDING)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: avoid leaving inactive connections when Home assistant fails to send a command a need to establish a new connection
# FUTURE IMPROVEMENT: controller.exec_cmd may return a Response object so each command can choose what status, description etc. to set


def build_websocket_handler(controller: Controller):
    logger = logging.getLogger(__name__)

    async def handler(request: Request):

        ws = WebSocketResponse()
        await ws.prepare(request)
        logger.info(f'New client connected from {request.get_extra_info("peername", request.remote)}')
        logger.info('Ready to receive commands from client')

        parser = CommandParser(controller)

        async for msg in ws:

            if msg.type != aiohttp.WSMsgType.TEXT: 
                logger.error(f'Message received with an invalid WebSocket message type: {msg.type.name}')
                response = Error(status=HTTPStatus.BAD_REQUEST, description=f'Message type {msg.type.name} not valid for commands, use TEXT')
                await ws.send_json(asdict(response))
            else:
                response = Error(HTTPStatus.INTERNAL_SERVER_ERROR)

                try:
                    cmd = parser.parse(msg.data)
                    logger.debug(f'Command received : {msg.data}')
                    if not isinstance(cmd, Disconnect):
                        cmd.validate_arguments()
                        result = controller.exec_cmd(cmd)
                        response = Response(status=HTTPStatus.ACCEPTED, data=result)
                    else:
                        # TODO: check if this close the socket correctly
                        await ws.close()

                except ApiError as e:
                    logger.warning('', exc_info=e)
                    response = Error(status=e.status, description=e.message)
                except Exception as e:
                    logger.exception(e)
                finally:
                    await ws.send_json(asdict(response))

    return handler


if __name__ == '__main__':
    config = load_config()
    host = config['DEFAULT'].get('host', '0.0.0.0')
    port = int(config['DEFAULT'].get('port', str(8080)))
    default_gateway = config['CONNECTION_CHECK'].get('default_gateway')
    iface = config['CONNECTION_CHECK'].get('iface')
    timeout = float(config['CONNECTION_CHECK'].get('timeout'))
    status_led = int(config['CONNECTION_CHECK'].get('status_led'))

    configure_logging(config)
    configure_status_led(config)

    # Using the controller to handle the strip is thread-safe under the assumption that there's only 
    # one thread managing the event loop.
    controller = Controller(config)
    exit_code = 0
    logger = logging.getLogger("main")

    try:
        turn_led_indicator_off(status_led)
        reply = sr1(IP(dst=default_gateway)/ICMP(), iface=iface, timeout=timeout, verbose=False)
        if reply is None: 
            raise Exception(f"No answer from {default_gateway}")
        turn_led_indicator_on(status_led)

        app = Application()
        app.add_routes([get('/', build_websocket_handler(controller))])
        run_app(app, print=logger.info)

    except Exception as e:
        logger.exception(e)
        exit_code = 1
    finally:
        logger.info('Finalizing server')
        cleanup_gpio()
        exit(exit_code)
