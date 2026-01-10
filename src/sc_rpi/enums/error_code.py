"""Contains the ErrorCode class."""

from enum import Enum

# TODO: use strings instead of numbers for API users

class ErrorCode(Enum):
    """Error codes for the user."""

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    PARSE_ERROR = "PARSE_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    SECTION_OVERLAPPING = "SECTION_OVERLAPPING"
    SECTION_NOT_FOUND = "SECTION_NOT_FOUND"
    COMMAND_NOT_FOUND = "COMMAND_NOT_FOUND"
    INVALID_COLOR = "INVALID_COLOR"
    INVALID_COMMAND = "INVALID_COMMAND"
