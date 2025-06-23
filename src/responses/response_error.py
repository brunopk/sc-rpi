"""Error response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from .response import Response

if TYPE_CHECKING:
    from http import HTTPStatus

    from enums import ErrorCode


class Error(TypedDict, total=False):
    """Error payload."""

    code: ErrorCode

    description: str

@dataclass
class ResponseError(Response):
    """Error response for all commands."""

    def __init__(
        self,
        status: HTTPStatus,
        payload: Error,
        command: str | None = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus):    Status code (same status codes used in HTTP).
            payload (Error):    Contains the error code which indicates what is
                                the error about and a description for more
                                information (optional).
            command (str | None, optional): Indicates for which command is the response.
            description (str | None): Message for the user. Defaults to None.

        """
        super().__init__(status, command=command, payload=payload)
