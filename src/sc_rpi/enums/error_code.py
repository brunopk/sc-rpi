"""Contains the ErrorCode class."""

from enum import Enum

# TODO: use strings instead of numbers for API users

class ErrorCode(Enum):
    """Error codes for the user."""

    INTERNAL_SERVER_ERROR = 1
    PARSE_ERROR = 2
    BAD_REQUEST = 3
    SECTION_OVERLAPPING = 4
    SECTION_NOT_FOUND = 5
    COMMAND_NOT_FOUND = 6
    INVALID_COLOR = 7
    INVALID_COMMAND = 8
