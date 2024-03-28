import logging
import aiohttp

from aiohttp import web as _web
from dataclasses import asdict
from command import CommandParser
from response import Response, Error
from errors import ApiError
from http import HTTPStatus
from commands.disconnect import Disconnect
from hardware_controller import HardwareController

# TODO: TEST all commands (turn_off DONE, turn_on DONE)
# TODO: combine module command and package commands into one
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: update doc to explain that SCP custom protocol is replaced by Websocket
# FUTURE IMPROVEMENT: controller.exec_cmd may return a Response object so each command can choose what status, description etc. to set

def build_websocket_handler(hw_controller: HardwareController):

    logger = logging.getLogger(__name__)

    async def handler(request: _web.Request):

        ws = _web.WebSocketResponse()
        await ws.prepare(request)
        logger.info(f'New client connected from {request.get_extra_info("peername", request.remote)}')
        logger.info('Ready to receive commands from client')

        parser = CommandParser()

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
                        result = hw_controller.exec_cmd(cmd)
                        response = Response(status=HTTPStatus.ACCEPTED, data=result)
                    else:
                        # TODO: check if this close the socket correctly
                        await ws.close() 
                    
                except ApiError as e:
                    logger.warning(f'Error:', exc_info=e)
                    response = Error(status=e.status, description=e.message)
                except Exception as e:
                    logger.exception(e)
                finally:
                    await ws.send_json(asdict(response))

    return handler

