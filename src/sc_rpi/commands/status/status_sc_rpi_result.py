"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.results.status import Status
from sc_rpi.commands.sc_rpi_base_result import ScRpiBaseResult

if TYPE_CHECKING:
    from http import HTTPStatus


@dataclass
class StatusScRpiResult(ScRpiBaseResult[Status]):
    """Contains available sections."""

    payload: Status

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        status: Status,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            status (Status): The result of the command.

        """
        super().__init__(status_code, command_name, status, None)
