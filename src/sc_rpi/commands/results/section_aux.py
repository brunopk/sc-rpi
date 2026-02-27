"""Contains the `SectionAux` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.models.color import Color

# TODO: move this class to sc_rpi_status_result and rename to Section

@dataclass
class SectionAux:
    """Represents a section of leds in the strip."""

    id: str

    start: int

    end: int

    color: Color

    is_on: bool
