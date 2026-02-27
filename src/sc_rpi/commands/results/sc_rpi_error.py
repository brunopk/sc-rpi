"""Contains the `Error` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.enums.error_code import ErrorCode

# TODO: move this class to sc_rpi_base_result and rename as Error

@dataclass
class ScRpiError:
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str
