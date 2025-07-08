"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Help:
    """Contain helpful information for users."""

    commands: list[str]
