"""Contains the `TurnSectionOnArgs` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.utils import is_valid_color

# TODO: CONTINUE: get the color and turn the strip with this color
# TODO: CONTINUE: run all unit test to see if nothing is broken

@dataclass
class TurnSectionOnArgs:
    """`turn_section_on` command arguments."""

    section_id: str

    color: Optional[str] = None

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        if self.color is not None and not is_valid_color(self.color):
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_COLOR)


