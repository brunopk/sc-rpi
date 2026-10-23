"""Main class: `HelpResult`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.results import Result

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class HelpResultPayload:
    """Contain helpful information for users."""

    commands: list[str]

@dataclass
class HelpResult(Result[HelpResultPayload]):
    """Response for the `help` command."""

    payload: HelpResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: HelpResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (HelpResultPayload): The result of the command.

        """
        super().__init__(status_code, command_name, payload, None)
