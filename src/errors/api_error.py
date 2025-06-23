"""Generic error object for all commands."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from http import HTTPStatus

    from enums import ErrorCode


class ApiError(Exception):
    """Generic error object for all commands."""

    def __init__(
        self,
        status: HTTPStatus,
        code: ErrorCode,
        message: str | None = None,
        *args: object,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): HTTP status code for the user
            code (ErrorCode): Error code for the user
            message (str | None, optional): Message for the user. Defaults to None.
            *args (object): Extra arguments.

        """
        super().__init__(*args)
        self.status = status
        self.code = code
        self.message = message