"""Contains the `SectionAux` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.models.color import Color

# TODO: move this into a new models.response package

@dataclass
class SectionAux:
    """Represents a section of leds in the strip."""

    ha_entity_id: str

    start: int

    end: int

    color: Color

    is_on: bool
