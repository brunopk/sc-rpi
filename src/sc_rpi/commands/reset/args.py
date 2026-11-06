"""Contains the `ResetArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResetArgs:
    """`reset` command arguments."""

    name: str | None = None
