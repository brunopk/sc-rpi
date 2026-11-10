"""Contains the `SaveConfigArgs` class."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SaveConfigArgs:
    """Arguments for the `save_config` command."""

    name: str | None = None
    """Name to save the config as. When omitted, the active configuration's name."""

    description: str = field(default="")

    overwrite: bool = False
    """Replace the saved config if the name is taken."""
