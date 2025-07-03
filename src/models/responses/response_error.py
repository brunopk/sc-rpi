"""Error response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .response import Response

if TYPE_CHECKING:
    from http import HTTPStatus

    from .error import Error


@dataclass
class ResponseError(Response):
    """Error response for all commands."""

    error: Error

    def __init__(self, status: HTTPStatus, error: Error) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            error (Error): Error object.

        """
        super().__init__(status)
        self.error = error
