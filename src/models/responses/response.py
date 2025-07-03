"""Generic response for all commands.

It may be an error (instance of `ResponseError`) or
a successful response (instance of `ResponseOk`)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from http import HTTPStatus


@dataclass
class Response:
    """Generic response for all commands.

    It may be an error (instance of `ResponseError`) or
    a successful response (instance of `ResponseOk`)
    """

    status: int

    command: str | None

    def __init__(self, status: HTTPStatus) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP)

        """
        self.status = status.value
