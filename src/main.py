#!/usr/bin/env python3

from command import CommandParser
from network import NetworkManager, ClientDisconnected
from response import Response
from error import ParseError, ExecutionError, ValidationError
from http import HTTPStatus
from commands.disconnect import Disconnect
from controller import Controller
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler
from logging import Formatter, basicConfig, getLogger, StreamHandler

if __name__ == '__main__':

    config = ConfigParser()
    config.read('../config.ini')
    ctrl = Controller(config)
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
    formatter = Formatter(log_format)
    fileHandler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
    consoleHandler = StreamHandler()
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    handlers = [fileHandler, consoleHandler] if log_on_console else [fileHandler]
    # noinspection PyArgumentList
    basicConfig(level=level, handlers=handlers)
    logger = getLogger('Main')
    logger.info('Starting')

    try:

        network_manager.start()

        while True:

            network_manager.accept_client()
            logger.info('Ready to receive commands from client')

            while True:

                try:
                    req = network_manager.receive()
                    cmd = parser.parse(req)
                    logger.info(f'Command received: {req[0:-1]}')
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
