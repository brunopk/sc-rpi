"""Successful response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .response import Response

if TYPE_CHECKING:
    from http import HTTPStatus


@dataclass
class ResponseOk(Response):
    """Successful response for all commands."""

    def __init__(
        self,
        status: HTTPStatus,
        command: str,
        payload: dict | None = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP)
            command (str): Indicates for which command is the response.
            payload (dict | None, optional):    The result payload specific to
                                                the command. Defaults to None.

        """
        super().__init__(status, command, payload)
