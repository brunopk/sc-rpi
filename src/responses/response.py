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

    status: HTTPStatus

    command: str | None

    payload: dict | None

    def __init__(
        self,
        status: HTTPStatus,
        command: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP)
            command (str | None, optional): Indicates for which command is the response.
            payload (dict | None, optional): The result payload specific to the command.

        """
        self.status = status
        self.command = command
        self.payload = payload
