"""Contains the `HelpResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.available.help.help_sc_rpi_result_payload import (
  HelpScRpiResultPayload,
)
from sc_rpi.commands.results.sc_rpi_base_result import ScRpiBaseResult

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class HelpScRpiResult(ScRpiBaseResult[HelpScRpiResultPayload]):
    """Response for the `help` command."""

    payload: HelpScRpiResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        help_sc_rpi_result_payload: HelpScRpiResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            help_sc_rpi_result_payload (HelpScRpiResultPayload): The result of a \
                command.

        """
        super().__init__(status_code, command_name, help_sc_rpi_result_payload, None)
