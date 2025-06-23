"""Contains the ErrorCode class."""

from enum import Enum


class ErrorCode(Enum):
    """Error codes for the user."""

    INTERNAL_ERROR = 1
    ALREADY_OFF = 2
    ALREADY_ON = 3
    OVERLAPPING = 4
    PARSE_ERROR = 5
    BAD_REQUEST = 6
    SECTION_NOT_FOUND = 7
