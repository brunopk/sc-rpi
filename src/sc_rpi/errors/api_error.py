"""Generic error object for all commands."""

from __future__ import annotations

from http import HTTPStatus

from sc_rpi.enums import ErrorCode


class ApiError(Exception):
    """Generic error object for all commands."""

    def __init__(
        self,
        status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
        message: str | None = None,
        *args: object,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus, optional): HTTP status code for the user.
                Defaults to HTTPStatus.INTERNAL_SERVER_ERROR.
            code (ErrorCode, optional): Error code for the user.
                Defaults to ErrorCode.INTERNAL_ERROR.
            message (str | None, optional): Message for the user. Defaults to None.
            *args: Optional arguments.

        """
        super().__init__(*args)
        self.status = status
        self.code = code
        self.message = message
