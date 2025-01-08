import logging
import logging.handlers

from configparser import ConfigParser
from re import match
from typing import Tuple

import RPi.GPIO as GPIO

from systemd.journal import JournalHandler
from webcolors import hex_to_rgb

ENV_DEV = "dev"
ENV_PROD = "rpi"
AVAILABLE_ENVIRONMENTS = [ENV_DEV, ENV_PROD]


def load_config() -> ConfigParser :
    config = ConfigParser()
    config.read('./config.ini')

    if config['CONNECTION_CHECK'].get('status_led') is None:
        raise Exception('Property status_led not set')
    if config['CONNECTION_CHECK'].get('default_gateway') is None:
        raise Exception('Property default_gateway in section CONNECTION not set')
    if config['CONNECTION_CHECK'].get('iface') is None:
        raise Exception('Property iface in section CONNECTION not set')
    if config['CONNECTION_CHECK'].get('timeout') is None:
        raise Exception('Property timeout in section CONNECTION not set')
    if config['DEFAULT'].get('env') is None:
        raise Exception('Property env in DEFAULT section not set')
    elif config['DEFAULT'].get('env') not in AVAILABLE_ENVIRONMENTS:
        raise Exception(f'\'{config["DEFAULT"].get("env")}\' is not valid, it must be one of these: ${AVAILABLE_ENVIRONMENTS}')

    return config

def configure_logging(config: ConfigParser):
    level = config['LOGGING'].get('level', 'ERROR')

    handlers = []
    if config['DEFAULT'].get('env') == ENV_DEV:
        console_handler = logging.StreamHandler()
        console_handler.emit = __decorate_console_handler_emit(console_handler.emit)

        log_format = '%(asctime)s - %(name)s - %(levelname)s -- %(message)s'
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        handlers.append(console_handler)
    else:
        handlers.append(JournalHandler())

    logging.basicConfig(level=level, handlers=handlers)

def configure_status_led(config: ConfigParser):
    pin_number = int(config['CONNECTION_CHECK'].get('status_led'))
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin_number, GPIO.OUT)

def turn_led_indicator_on(pin_number: int):
    GPIO.output(pin_number, GPIO.HIGH)

def turn_led_indicator_off(pin_number: int):
    GPIO.output(pin_number, GPIO.LOW)

def cleanup_gpio():
    GPIO.cleanup()

def parse_color(c: str) -> Tuple[int, int, int]:
    """
    Parse and returns the corresponding color

    :param c: RGB or hexadecimal string representation of the color
    :return: the color
    :raises ValueError: if c is not correctly defined
    """
    try:
        c = hex_to_rgb(c)
        (red, green, blue) = c.red, c.green, c.blue
    except ValueError:
        regex_rgb = r"^rgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$"
        _match = match(regex_rgb, c)
        if _match is not None:
            red = int(_match.groups()[0])
            green = int(_match.groups()[1])
            blue = int(_match.groups()[2])
            if 0 > red or 0 > green or 0 > blue or 255 < red or 255 < green or 255 < blue:
                raise ValueError()
        else:
            raise ValueError()
    return red, green, blue

def parse_bool(b: str):
    """
    Parse a string as bool:

        - 'True', 'true', 'y' , '1' -> True
        - 'False', 'false', 'n', '0' -> False

    :raise ValueError: if string cannot be parsed as detailed above
    """
    if b in ['True', 'true', 'y' , '1']:
        return True
    elif b in ['False', 'false', 'n', '0']:
        return False
    else:
        raise ValueError()

def __decorate_console_handler_emit(fn):
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
