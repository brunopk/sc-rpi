"""Contains the `Section` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of leds in the strip."""

    end: int

    id: str

    name: str

    start: int
