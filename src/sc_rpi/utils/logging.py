"""Utility functions to set logging configurations."""

import logging
import sys
from logging import basicConfig
from logging.handlers import SysLogHandler

import structlog
from colorama import Fore, Style, init
from structlog.dev import ConsoleRenderer

from sc_rpi.config import Config

init(autoreset=True)

_LEVEL_COLORS = {
    "debug": Fore.CYAN,
    "info": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "critical": Fore.MAGENTA,
}

def _level_formatter(_, value):
    color = _LEVEL_COLORS.get(value, "")
    return f"{color}[{value.upper()}]{Style.RESET_ALL}"

def _logger_name_formatter(_, value):
    return f"{value} : "

def configure_logging(config: Config) -> None:
    """Configure the `logging` library.

    Args:
        config (Config): SC RPI configurations

    Returns:
        _type_: _description_

    """
    level = config.log_level
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
    ]

    if config.env == "prod":
        # TODO: test if this works with Loki
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.LogfmtRenderer(),
            foreign_pre_chain = shared_processors,
        )
        handler = SysLogHandler(address="/dev/log")
    elif config.env == "dev":
        # The "" column is for extra fields
        # passed as extra arguments to info(), debug(), etc.
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=ConsoleRenderer(
                columns=[
                    structlog.dev.Column("timestamp", formatter=lambda _, v: str(v)),
                    structlog.dev.Column("level", formatter=_level_formatter),
                    structlog.dev.Column("logger", formatter=_logger_name_formatter),
                    structlog.dev.Column("event", formatter=lambda _, v: str(v)),
                    structlog.dev.Column("", formatter=lambda _, v: str(v)),
            ]),
            foreign_pre_chain=shared_processors,
        )
        handler = logging.StreamHandler(sys.stdout)
    else:
        raise Exception(f"Unknown environment {config.env} use prod or dev")

    handler.setFormatter(formatter)
    basicConfig(level=level, handlers=[handler])

def collapse_multiline_str_into_one_line(long_message: str) -> str:
    """Collapse a multiline (defined between triple `"`) into a one-line string.

    Useful to log long messages.

    Args:
        long_message (str): Multi line string to be transformed.

    Returns:
        str: Transformed string (one-line)

    """
    return " ".join(long_message.split())

__all__ = ["collapse_multiline_str_into_one_line", "configure_logging"]
