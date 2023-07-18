from enum import Enum


class ErrorCode(Enum):
    ALREADY_OFF = 1
    ALREADY_ON = 2
    EXECUTION_ERROR = 3
    OVERLAPPING = 4
    PARSE_ERROR = 6
    BAD_REQUEST = 7
    SECTION_NOT_FOUND = 8
