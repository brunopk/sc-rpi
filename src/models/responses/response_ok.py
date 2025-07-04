"""Successful response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .response import Response

if TYPE_CHECKING:
    from http import HTTPStatus
    from typing import Any


@dataclass
class ResponseOk(Response):
    """Successful response for all commands."""

    data: Any | None

    def __init__(self, status: HTTPStatus, data: Any | None = None) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP)
            data (Any | None, optional): The result of a command. Defaults to None.

        """
        super().__init__(status)
        self.data = data
