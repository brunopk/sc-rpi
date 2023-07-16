#!/usr/bin/env python3

import logging
import logging.handlers

from command import CommandParser
from network import NetworkManager, ClientDisconnected
from response import Response
from errors import ApiError, ParseError, ValidationError
from http import HTTPStatus
from commands.disconnect import Disconnect
from controller import Controller
from configparser import ConfigParser


def decorate_console_handler_emit(fn):
    """
    Based on Stack Overflow post: 
    https://stackoverflow.com/questions/20706338/color-logging-using-logging-module-in-python
    """
    def new(*args):
        levelno = args[0].levelno
        if levelno >= logging.CRITICAL:
            color = '\x1b[31;1m'
        elif levelno >= logging.ERROR:
            color = '\x1b[31;1m'
        elif levelno >= logging.WARNING:
            color = '\x1b[33;1m'
        else:
            color = '\x1b[0m'

        args[0].msg = "{0}{1}\x1b[0m".format(color, args[0].msg)
        args[0].levelname = "{0}{1}\x1b[0m".format(color, args[0].levelname)

        return fn(*args)
    return new


if __name__ == '__main__':

    config = ConfigParser()
    config.read('../config.ini')
    network_manager = NetworkManager(config)
    parser = CommandParser()

    # Logging configuration

    level = config['LOGGING'].get('level', 'ERROR')
    log_on_console = config['LOGGING'].get('console', False)
    log_on_console = log_on_console == '1' or log_on_console == 'True' or log_on_console == 'true'
    filename = config['LOGGING'].get('filename', '/var/log/sc_driver.log')
    max_bytes = int(config['LOGGING'].get('max_bytes', str(1024 * 1024)))
    backup_count = int(config['LOGGING'].get('backup_count', str(5)))
    log_format = '%(asctime)s - %(name)s - %(levelname)s -- %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=max_bytes,
        backupCount=backup_count)
    console_handler = logging.StreamHandler()
    console_handler.emit = decorate_console_handler_emit(console_handler.emit)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    handlers = [file_handler, console_handler] if log_on_console else [file_handler]
    # noinspection PyArgumentList
    logging.basicConfig(level=level, handlers=handlers)
    logger = logging.getLogger('Main')
    logger.info('Starting')

    try:

        network_manager.start()

        while True:

            network_manager.accept_client()
            ctrl = Controller(config)
            logger.info('Ready to receive commands from client')

            while True:

                try:
                    req = network_manager.receive()
                    cmd = parser.parse(req)
                    if not isinstance(cmd, Disconnect):
                        cmd.validate_arguments()
                        result = ctrl.exec_cmd(cmd)
                        response = Response(HTTPStatus.OK, result)
                        network_manager.send(response)
                    else:
                        network_manager.stop()
                        break
                except ParseError as e:
                    logger.warning('Invalid command received')
                    response = Response(HTTPStatus.BAD_REQUEST, e.errors)
                    network_manager.send(response)
                except ValidationError as e:
                    logger.warning('Invalid command received')
                    response = Response(HTTPStatus.BAD_REQUEST, e.get_msg())
                    network_manager.send(response)
                except ExecutionError as e:
                    response = Response(HTTPStatus.CONFLICT, {'error': e.get_msg()})
                    network_manager.send(response)
                except ClientDisconnected as e:
                    network_manager.disconnect_client()
                    break
                except ConnectionResetError:
                    logger.warning('Client disconnected abruptly')
                    break
                except Exception as e:
                    response = Response(HTTPStatus.INTERNAL_SERVER_ERROR, {'error': 'Internal server error'})
                    network_manager.send(response)
                    logger.exception(e)

    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        network_manager.stop()
