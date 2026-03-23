"""Utility functions to set logging configurations."""

import logging
from logging import Formatter, StreamHandler, basicConfig
from logging.handlers import QueueHandler
from multiprocessing import Queue

from sc_rpi.models.config import Config


def configure_logging(config: Config) -> None:
    """Configure the `logging` library.

    Args:
        config (Config): SC RPI configurations

    Returns:
        _type_: _description_

    """
    level = config.log_level

    if config.env == "prod":

        log_format = "%(message)s"
        formatter = Formatter(log_format)
        queue = Queue(-1)
        queue_handler = QueueHandler(queue)
        queue_handler.setFormatter(formatter)

        # TODO: CONTINUE
        # TODO: summarize documentation about Loki in linux_dependencies.md
        # TODO: explain in raspberry_pi.md that 64 bit version of Raspberry Pi OS is required for [Grafana Loki](doc/linux_dependencies.md#loki).

        """loki = LokiLogger(
            url="http://loki:3100/loki/api/v1/push",
            labels={"app": "my-app"},
            batch_size=100,
            flush_interval=2
        )"""
        basicConfig(level=level, handlers=[])
        return

    stream_handler = StreamHandler()
    stream_handler.emit = _decorate_console_handler_emit(stream_handler.emit)

    log_format = "%(asctime)s - %(name)s - %(levelname)s -- %(message)s"
    formatter = Formatter(log_format)
    stream_handler.setFormatter(formatter)

    basicConfig(level=level, handlers=[stream_handler])

def collapse_multiline_str_into_one_line(long_message: str) -> str:
    """Collapse a multiline (defined between triple `"`) into a one-line string.

    Useful to log long messages.

    Args:
        long_message (str): Multi line string to be transformed.

    Returns:
        str: Transformed string (one-line)

    """
    return " ".join(long_message.split())

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
