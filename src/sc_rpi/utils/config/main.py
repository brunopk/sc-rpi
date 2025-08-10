"""Contains helper functions."""

from __future__ import annotations

import logging
from pathlib import Path

import RPi.GPIO as GPIO
import yaml
from systemd.journal import JournalHandler

from sc_rpi.errors import ApiError
from sc_rpi.models.config import Config

"""Load all configurations from `config.ini` file."""

def load_configurations() -> Config:
    """Load all configurations from `config.ini` file.

    Raises:
        ApiException:

    Returns:
        Config: Return a `Config` instance with loaded configurations.

    """
    try:
        with Path.open(Path("config.yaml")) as f:
            config_dict = yaml.load(f, Loader=yaml.SafeLoader)
            return Config.from_dict(config_dict)
    except KeyError as ex:
        raise ApiError from ex
    except Exception as ex:
        raise ApiError from ex

def configure_logging(config: Config) -> None:
    """Configure the `logging` library.

    Args:
        config (Config): SC RPI configurations

    Returns:
        _type_: _description_

    """
    level = config.log_level

    handlers = []
    if config.env == "dev":
        console_handler = logging.StreamHandler()
        console_handler.emit = _decorate_console_handler_emit(console_handler.emit)

        log_format = "%(asctime)s - %(name)s - %(levelname)s -- %(message)s"
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        handlers.append(console_handler)
    else:
        handlers.append(JournalHandler())

    logging.basicConfig(level=level, handlers=handlers)

def configure_status_led(config: Config):
    """Configure status led."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(config.status_led, GPIO.OUT)

def _decorate_console_handler_emit(fn):
    """Based on Stack Overflow post: \

    https://stackoverflow.com/questions/20706338/color-logging-using-logging-module-in-python.

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
