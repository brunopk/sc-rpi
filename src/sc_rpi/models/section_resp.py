"""Contains the `SectionResp` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SectionResp:
    """Represents a section of leds in the strip."""

    ha_entity_id: str

    start: int

    end: int

    color: str

    is_on: bool
