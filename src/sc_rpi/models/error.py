"""Contains the `Error` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sc_rpi.enums import ErrorCode

# TODO: move this into a new models.response package

@dataclass
class Error:
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str
