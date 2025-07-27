"""Contains the `Section` class."""

import re
from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError


@dataclass
class Section:
    """Defines a section in the strip. \

    Used for `add_section` command arguments.
    """

    start: int

    end: int

    color: str

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        if not re.fullmatch(r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", self.color):
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_COLOR)

