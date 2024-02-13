import logging

from scapy.all import IP, ICMP, sr1
from command import CommandParser
from network import NetworkManager, ClientDisconnected
from response import Response, Error
from errors import ApiError
from http import HTTPStatus
from commands.disconnect import Disconnect
from controller import Controller
from helpers import configure_logging, configure_status_led, load_config, turn_led_indicator_on, turn_led_indicator_off, cleanup_gpio

# TODO: TEST all commands
# TODO: FIX LINES 97 101 AND CATCH ApiError to return the corresponding response
# TODO: actualizar documentacion para indicar que todos los comandos devuelven el mismo formato para errores {status: XXX, message: 'adasd'}


def run():
    config = load_config()
    default_gateway = config['CONNECTION_CHECK'].get('default_gateway')
    iface = config['CONNECTION_CHECK'].get('iface')
    timeout = float(config['CONNECTION_CHECK'].get('timeout'))
    status_led = int(config['CONNECTION_CHECK'].get('status_led'))
    
    configure_logging(config)
    logger = logging.getLogger(__name__)
    logger.info('Starting server')

    parser = CommandParser()
    network_manager = NetworkManager(config)

    configure_status_led(config)

    try:
       
        turn_led_indicator_off(status_led)
        reply = sr1(IP(dst=default_gateway)/ICMP(), iface=iface, timeout=timeout, verbose=0)
        if reply is None: 
            logging.error(f"No answer from {default_gateway}")
            exit(1)
        turn_led_indicator_on(status_led)
        
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
                        response = Response(result)
                        network_manager.send(response)
                    else:
                        network_manager.stop()
                        break
                except ApiError as e:
                    logger.warning(f'API Error', exc_info=e)
                    response = Error(HTTPStatus.INTERNAL_SERVER_ERROR)
                    try:
                        response = Error(status=HTTPStatus(e.status), description=e.message)
                    except Exception as ex:
                        logger.exception(ex)
                    network_manager.send(response)
                except ClientDisconnected as e:
                    network_manager.disconnect_client()
                    break
                except ConnectionResetError:
                    logger.warning('Client disconnected abruptly')
                    break
                except Exception as e:
                    response = Error(HTTPStatus.INTERNAL_SERVER_ERROR)
                    network_manager.send(response)
                    logger.exception(e)

    except KeyboardInterrupt as e:
        logger.info('Finalizing server...')
    except Exception as e:
        logger.exception(e)
    finally:
        network_manager.stop()
        cleanup_gpio()
