"""Contains the `GetConfigResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.models.commands.all.get_config.get_config_sc_rpi_result_payload import (
  GetConfigScRpiResultPayload,
)
from sc_rpi.models.commands.command_result.sc_rpi_result import ScRpiResult

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class GetConfigScRpiResult(ScRpiResult[GetConfigScRpiResultPayload]):
    """Contains available sections."""

    payload: GetConfigScRpiResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        get_config_sc_rpi_result_payload: GetConfigScRpiResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            get_config_sc_rpi_result_payload (GetConfigScRpiResultPayload): The result \
              of a command.

        """
        super().__init__(
            status_code,
            command_name,
            get_config_sc_rpi_result_payload,
            None,
        )
