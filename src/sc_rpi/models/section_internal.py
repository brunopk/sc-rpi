"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SectionInternal:
    """Represents a set of leds in the strip.

    This class is intended for internal use, not for API users.
    """

    id: str

    limits: tuple[int, int]

    color_list: list[tuple[int, int, int]]

    is_on: bool
