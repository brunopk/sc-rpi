"""Utility functions to set logging configurations."""

import logging

from systemd.journal import JournalHandler

from sc_rpi.models.config import Config


def configure_logging(config: Config) -> None:
    """Configure the `logging` library.

    Args:
        config (Config): SC RPI configurations

    Returns:
        _type_: _description_

    """
    level = config.log_level
    handler = logging.StreamHandler()
    if config.env == "prod":
        handler = JournalHandler()

    handler.emit = _decorate_console_handler_emit(handler.emit)
    log_format = "%(asctime)s - %(name)s - %(levelname)s -- %(message)s"
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[handler])

def _decorate_console_handler_emit(fn):
    """Based on Stack Overflow post: \

    https://stackoverflow.com/questions/20706338/color-logging-using-logging-module-in-python.

    """
    def new(*args):
        level_no = args[0].levelno
        if level_no >= logging.CRITICAL:
            args[0].levelname = f"\x1b[1;31m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.ERROR:
            args[0].levelname = f"\x1b[31m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.WARNING:
            args[0].levelname = f"\x1b[33m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.INFO:
            args[0].levelname = f"\x1b[32m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.DEBUG:
            args[0].levelname = f"\x1b[35m{args[0].levelname}\x1b[0m"

        return fn(*args)
    return new
