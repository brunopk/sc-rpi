"""Contains Error class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import ErrorCode

@dataclass
class Error:
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str
