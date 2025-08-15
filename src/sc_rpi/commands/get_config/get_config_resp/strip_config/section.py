"""Contains the `Section` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of leds in the strip."""

    ha_entity_id: str

    start: int

    end: int
