"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a set of leds in the strip."""

    id: str

    start: int

    end: int

    color: str

    is_on: bool
