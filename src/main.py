#!/usr/bin/env python3

from command import CommandParser, ParseError, ExecutionError
from network import NetworkManager, SCPError
from response import Response
from http import HTTPStatus
from commands.disconnect import Disconnect
from controller import Controller
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler
from logging import Formatter, basicConfig, getLogger

if __name__ == '__main__':

    config = ConfigParser()
    config.read('../config.ini')
    ctrl = Controller(config)
    network_manager = NetworkManager(config)
    parser = CommandParser()

    # Logging configuration
    level = config['LOGGING'].get('level', 'ERROR')
    filename = config['LOGGING'].get('filename', '/var/log/sc_driver.log')
    max_bytes = int(config['LOGGING'].get('max_bytes', str(1024 * 1024)))
    backup_count = int(config['LOGGING'].get('backup_count', str(5)))
    log_format = '%(asctime)s - %(name)s - %(levelname)s -- %(message)s'
    formatter = Formatter(log_format)
    handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    # noinspection PyArgumentList
    basicConfig(level=level, handlers=[handler])
    logger = getLogger()
    logger.info('Starting sc-driver')

    try:

        network_manager.start()

        while True:

            network_manager.accept()
            logger.info('Ready to receive commands from client')

            while True:

                try:
                    msg = network_manager.receive()
                    cmd = parser.parse(msg.get_body())
                    if not isinstance(cmd, Disconnect):
                        res = ctrl.exec_cmd(cmd)
                        res = Response(HTTPStatus.OK, res)
                        network_manager.send(res.to_json())
                    else:
                        network_manager.close()
                        break
                except SCPError as e:
                    res = Response(HTTPStatus.BAD_REQUEST, {'error': e.get_msg()})
                    network_manager.send(res.to_json())
                except ParseError as e:
                    res = Response(HTTPStatus.BAD_REQUEST, e.errors)
                    network_manager.send(res.to_json())
                except ExecutionError as e:
                    res = Response(HTTPStatus.INTERNAL_SERVER_ERROR, {'error': e.get_msg()})
                    network_manager.send(res.to_json())
                except Exception as e:
                    res = Response(HTTPStatus.INTERNAL_SERVER_ERROR, {'error': 'Internal server error'})
                    logger.exception(e)

    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        network_manager.close()
