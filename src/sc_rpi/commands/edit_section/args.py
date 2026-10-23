"""Contains the `EditSectionArgs` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models.color import Color
from sc_rpi.utils.colors import is_valid_color


@dataclass
class EditSectionArgs:
    """`edit_section` command arguments."""

    section_id: str

    start: Optional[int] = None

    end: Optional[int] = None

    color: Optional[Color] = None

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        if self.start is None and self.end is None and self.color is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "at least one attribute must not be null",
            )
        if self.color is not None and not is_valid_color(
            (self.color.r, self.color.g, self.color.b),
        ):
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_COLOR)

