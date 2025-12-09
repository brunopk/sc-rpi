"""Contains the `HelpResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.help.help_resp_payload import HelpRespPayload
from sc_rpi.models.response import Response

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class HelpResp(Response[HelpRespPayload]):
    """Response for the `help` command."""

    payload: HelpRespPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        help_resp_payload: HelpRespPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            help_resp_payload (HelpRespPayload): The result of a command.

        """
        super().__init__(status_code, command_name, help_resp_payload, None)
