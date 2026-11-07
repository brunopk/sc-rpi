"""Contains the `SaveConfigArgs` class."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SaveConfigArgs:
    """Arguments for the `save_config` command."""

    name: str | None = None

    description: str = field(default="")

