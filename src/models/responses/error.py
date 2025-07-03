"""Contains Error class."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from enums import ErrorCode

class Error(TypedDict, total=False):
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str
