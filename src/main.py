#!/usr/bin/env python3

import sys
import logging
import argparse
import socket
import json
import config

from os.path import dirname,abspath
#from rpi_ws281x import Color, PixelStrip
#from m1.controller import Controller

if __name__ == '__main__':

    # TODO validate invalid arguments eg: -level=INFO
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel',
                        help='Logging level. Possible options : DEBUG, INFO, WARNING, ERROR, CRITICAL',
                        nargs=1,
                        type=str,
                        default='INFO')
    args = parser.parse_args()
    log_level = args.loglevel if type(args.loglevel) == str else args.loglevel[0]
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        print('Invalid logging level {level}'.format(level=log_level))
        parser.print_help()
        exit(1)

    # Create NeoPixel object with appropriate configuration.
    #strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    #strip.begin()
    #controller = Controller(strip)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.bind((RPI_WS281x_HOST, RPI_WS281x_PORT))
    #server_socket.listen(TCP_MAX_QUEUE)

    logging.basicConfig(level=log_level)

    #print('Listening on IP address {ip} and port {port}.'.format(ip=RPI_WS281x_HOST, port=RPI_WS281x_PORT))
    print('Press Ctrl-C to quit.')

    # noinspection PyBroadException
    try:
        while True:
            client_socket, address = server_socket.accept()
            logging.info('Client connected {address}'.format(address=address))

            # TODO Try not opening and closing to much TCP connections
            raw_cmd = ''
            #chunk = client_socket.recv(TCP_MAX_MSG_SIZE)
            #while chunk.__len__() > 0:
            #    raw_cmd += chunk.decode(TCP_MSG_ENCODING)
            #    chunk = client_socket.recv(TCP_MAX_MSG_SIZE)
            client_socket.close()
            logging.info('Command received, raw command: {raw_cmd}'.format(raw_cmd=raw_cmd))

            # TODO Return error codes
            try:
                json_cmd = json.loads(raw_cmd)
                if 'action' in json_cmd:
                    action = json_cmd['action']
                    if action.__eq__('color'):
                        color = Color(json_cmd['red'], json_cmd['green'], json_cmd['blue'])
                        #controller.play_effect('static_color', color)
                    elif action.__eq__('effect'):
                        if 'name' in json_cmd:
                            effect_name = json_cmd['name']
                            #try:
                                #if effect_name.__eq__('blink_color'):
                                    #color = Color(json_cmd['red'], json_cmd['green'], json_cmd['blue'])
                                    #controller.play_effect('blink_color', color)
                                #else:
                                   #controller.play_effect(effect_name)
                            #except ModuleNotFoundError:
                                #logging.warning('Wrong effect name: {effect_name}'.format(effect_name=effect_name))
                        else:
                            logging.warning('Effect name undefined')

                    #elif action.__eq__('turn_off'):
                        #controller.turn_off_strip()
                    else:
                        logging.warning('Unrecognized action {action}'.format(action=action))
                else:
                    logging.warning('Action undefined')
            except ValueError:
                logging.warning('Error parsing {command} as JSON'.format(command=raw_cmd))

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception('ERROR')
    finally:
        print('Closing socket...')
        server_socket.close()
        print('Turning strip off...')
        #controller.turn_off_strip()
