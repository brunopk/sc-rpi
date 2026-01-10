"""Contains the `Error` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.enums.error_code import ErrorCode


@dataclass
class ScRpiError:
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str
