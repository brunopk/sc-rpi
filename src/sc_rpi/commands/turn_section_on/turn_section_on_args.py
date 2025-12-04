"""Contains the `TurnSectionOnArgs` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.color import Color
from sc_rpi.utils import is_valid_color


@dataclass
class TurnSectionOnArgs:
    """`turn_section_on` command arguments."""

    section_id: str

    color: Optional[Color] = None

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        if self.color is not None and not is_valid_color(
            (self.color.r, self.color.g, self.color.g),
        ):
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_COLOR)


