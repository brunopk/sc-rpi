"""Utility functions to set logging configurations."""

import logging
from logging import Formatter, StreamHandler, basicConfig
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue

from logging_loki import LokiHandler
from systemd.journal import JournalHandler

from sc_rpi.models.config import Config
from sc_rpi.utils.logging.ignore_loki_filter import IgnoreLokiFilter


# TODO: Explain how to install Grafana loki based on https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/
def configure_logging(config: Config) -> None:
    """Configure the `logging` library.

    Args:
        config (Config): SC RPI configurations

    Returns:
        _type_: _description_

    """
    level = config.log_level

    if config.env == "prod":
        journal_handler = JournalHandler()

        queue = Queue(-1)
        queue_handler = QueueHandler(queue)

        loki_handler = LokiHandler(
            url="http://localhost:3100/loki/api/v1/push",
            tags={"application": "my-app"},
            auth=("username", "password"),
            version="1",
        )
        loki_handler.addFilter(IgnoreLokiFilter())

        listener = QueueListener(queue, loki_handler)
        listener.start()

        basicConfig(level=level, handlers=[queue_handler, journal_handler])
        return

    stream_handler = StreamHandler()
    stream_handler.emit = _decorate_console_handler_emit(stream_handler.emit)

    log_format = "%(asctime)s - %(name)s - %(levelname)s -- %(message)s"
    formatter = Formatter(log_format)
    stream_handler.setFormatter(formatter)

    basicConfig(level=level, handlers=[stream_handler])


def _decorate_console_handler_emit(fn):
    """Based on Stack Overflow post: \

    https://stackoverflow.com/questions/20706338/color-logging-using-logging-module-in-python.

    """
    def new(*args):
        level_no = args[0].levelno
        if level_no >= logging.CRITICAL or level_no >= logging.ERROR:
            args[0].levelname = f"\x1b[1;31m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.WARNING:
            args[0].levelname = f"\x1b[1;33m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.INFO:
            args[0].levelname = f"\x1b[1;32m{args[0].levelname}\x1b[0m"
        elif level_no >= logging.DEBUG:
            args[0].levelname = f"\x1b[1;35m{args[0].levelname}\x1b[0m"

        return fn(*args)
    return new
