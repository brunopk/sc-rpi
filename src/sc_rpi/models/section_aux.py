"""Contains the `SectionAux` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SectionAux:
    """Represents a section of leds in the strip."""

    ha_entity_id: str

    start: int

    end: int

    color: str

    is_on: bool
