"""Contains the ErrorCode class."""

from enum import Enum


class ErrorCode(Enum):
    """Error codes for the user."""

    INTERNAL_ERROR = 1
    PARSE_ERROR = 2
    BAD_REQUEST = 3
    SECTION_OVERLAPPING = 4
    SECTION_NOT_FOUND = 5
