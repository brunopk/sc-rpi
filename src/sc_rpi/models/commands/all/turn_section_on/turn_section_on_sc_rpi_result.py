"""Contains the `TurnSectionOnResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.models.commands.command_result.sc_rpi_result import ScRpiResult
from sc_rpi.models.commands.command_result.status import Status

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class TurnSectionOnScRpiResult(ScRpiResult[Status]):
    """Contains available sections."""

    payload: Status

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        sc_rpi_result_payload: Status,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            sc_rpi_result_payload (Status): Payload for the result of a command.

        """
        super().__init__(status_code, command_name, sc_rpi_result_payload, None)
