"""Contains the `EditSectionArgs` class."""

from __future__ import annotations

import re
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError


@dataclass
class EditSectionArgs:
    """`edit_section` command arguments."""

    section_id: str

    start: Optional[int]

    end: Optional[int]

    color: Optional[str]

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        if self.color is not None and not re.fullmatch(
            r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", self.color,
        ):
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_COLOR)

