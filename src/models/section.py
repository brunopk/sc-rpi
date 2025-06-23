"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a set of leds in the strip."""

    id: str

    limits: tuple[int, int]

    color_list: list[tuple[int, int, int]]

    is_on: bool

    def __init__(
        self,
        section_id: str,
        limits: tuple[int, int],
        color_list: list[tuple[int, int, int]],
        *_args: str,
        is_on: bool = False,
    ) -> None:
        """Initialize the section.

        Args:
            section_id (str): Identifies the section.
            limits (tuple[int, int]): Defines the section (start and end position).
            color_list (list[tuple[int, int, int]]): Color for each led in the section
            is_on (bool): Indicates if the section is turned on.

        """
        self.id = section_id
        self.limits = limits
        self.color_list = color_list
        self.is_on = is_on
