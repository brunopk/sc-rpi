"""Contains the ErrorCode class."""

from enum import Enum


class ErrorCode(Enum):
    """Error codes for the user."""

    INTERNAL_ERROR = 1
    ALREADY_OFF = 2
    ALREADY_ON = 3
    PARSE_ERROR = 4
    BAD_REQUEST = 5
    SECTION_OVERLAPPING = 6
    SECTION_NOT_FOUND = 7
