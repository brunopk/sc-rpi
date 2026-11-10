"""Contains the `GetConfigArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GetConfigArgs:
    """`get_config` command arguments.

    `name` is required, but it is validated when the config is loaded (a missing name
    is reported as `MISSING_CONFIG_NAME` and an invalid one as `INVALID_CONFIG_NAME`).
    """

    name: str | None = None
