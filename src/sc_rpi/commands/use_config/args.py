"""Contains the `UseConfigArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UseConfigArgs:
    """`use_config` command arguments.

    `name` is validated when the config is applied (a missing name is reported as
    `MISSING_CONFIG_NAME`).
    """

    name: str | None = None
