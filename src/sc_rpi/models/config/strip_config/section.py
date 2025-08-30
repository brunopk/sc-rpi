"""Contains the `Section` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of leds in the strip."""

    end: int

    ha_entity_id: str

    ha_name: str

    start: int
