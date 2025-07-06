"""Contains helper functions."""

from __future__ import annotations

import logging
from configparser import ConfigParser

import RPi.GPIO as GPIO
from systemd.journal import JournalHandler

from sc_rpi.errors import ApiError
from sc_rpi.models.internal.config import Config, StripConfig

"""Load all configurations from `config.ini` file."""

def load_configurations() -> Config :
    """Load all configurations from `config.ini` file.

    Raises:
        ApiException:

    Returns:
        Config: Return a `Config` instance with loaded configurations.

    """
    try:
        config = ConfigParser()
        config.read("./config.ini")

        connection_timeout = config["MAIN"].getfloat("connection_timeout")
        default_gateway = config["MAIN"].get("default_gateway")
        default_network_interface = config["MAIN"].get("default_network_interface")
        env = config["MAIN"].get("env", "dev")
        host = config["MAIN"].get("host")
        log_level = config["MAIN"].get("log_level", "INFO")
        port = config["MAIN"].getint("port", 8080)
        status_led = config["MAIN"].getint("status_led", 17)

        brightness = config["PIXEL_STRIP"].getint("brightness", 255)
        channel = config["PIXEL_STRIP"].getint("channel", 0)
        dma = config["PIXEL_STRIP"].getint("dma", 10)
        freq_hz = config["PIXEL_STRIP"].getint("freq_hz", 800000)
        invert = config["PIXEL_STRIP"].getboolean("invert", False)
        pin = config["PIXEL_STRIP"].getint("pin", 18)
        strip_length = config["PIXEL_STRIP"].getint("strip_length")

        strip = _validate_strip_configuration(
            brightness, channel, dma, freq_hz, invert, pin, strip_length
        )
        return _validate_configurations(
            connection_timeout,
            default_gateway,
            default_network_interface,
            env,
            host,
            log_level,
            port,
            status_led,
            strip,
        )

    except ApiError:
        raise
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
        console_handler.emit = __decorate_console_handler_emit(console_handler.emit)

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

def __decorate_console_handler_emit(fn):
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

def _validate_configurations(
        connection_timeout: float | None,
        default_gateway: str | None,
        default_network_interface: str | None,
        env: str,
        host: str | None,
        log_level: str,
        port: int,
        status_led: int,
        strip: StripConfig) -> Config:

    dev = "dev"
    prod = "rpi"
    available_envs = [dev, prod]

    if env not in available_envs:
        raise ApiError(
            message=f"{env} must be one of these: ${available_envs}",
        )
    if connection_timeout is None:
        raise ApiError(message="connection_timeout not defined")
    if default_gateway is None:
        raise ApiError(message="default_gateway not defined")
    if default_network_interface is None:
        raise ApiError(message="default_network_interface not defined")
    if host is None:
        raise ApiError(message="host not defined")
    if status_led is None:
        raise ApiError(message="status_led not defined")

    return Config(
        connection_timeout,
        default_gateway,
        default_network_interface,
        env,
        host,
        log_level,
        port,
        status_led,
        strip,
    )

def _validate_strip_configuration(
    brightness: int | None,
    channel: int | None,
    dma: int | None,
    freq_hz: int | None,
    invert: bool | None,
    pin: int | None,
    strip_length: int | None,
) -> StripConfig:
    if brightness is None:
        raise ApiError(message="brightness not defined")
    if channel is None:
        raise ApiError(message="channel not defined")
    if dma is None:
        raise ApiError(message="dma not defined")
    if freq_hz is None:
        raise ApiError(message="freq_hz not defined")
    if invert is None:
        raise ApiError(message="invert not defined")
    if pin is None:
        raise ApiError(message="pin not defined")
    if strip_length is None:
        raise ApiError(message="strip_length not defined")

    return StripConfig(brightness, channel, dma, freq_hz, invert, pin, strip_length)
