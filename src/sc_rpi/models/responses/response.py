"""Successful response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from http import HTTPStatus
    from typing import Any

    from sc_rpi.models.responses import Error


@dataclass
class Response:
    """Response for all commands.

    It may be an error or a successful response.
    """

    status: int

    command_name: str | None

    payload: Any | None

    error: Error | None

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        payload: Any | None = None,
        error: Error | None = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (Any | None, optional): The result of a command. Defaults to None.
            error (Error | None, optional): Error object. Use it only if the command \
                failed (`payload` and `error` cannot be set at the same time). \
                    Defaults to None.

        """
        self.status = status.value
        self.payload = payload
        self.error = error
        self.command_name = command_name
