"""Contains the `GetConfigArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GetConfigArgs:
    """`get_config` command arguments.

    `name` is validated when the config is loaded (an invalid name is reported as
    `INVALID_CONFIG_NAME`).
    """

    name: str | None = None
