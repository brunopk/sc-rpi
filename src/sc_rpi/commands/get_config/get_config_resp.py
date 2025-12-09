"""Contains the `GetConfigResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.get_config.get_config_resp_payload import GetConfigRespPayload
from sc_rpi.models.response import Response

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class GetConfigResp(Response[GetConfigRespPayload]):
    """Contains available sections."""

    payload: GetConfigRespPayload

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        payload: GetConfigRespPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (GetConfigRespPayload): The result of a command.

        """
        super().__init__(status, command_name, payload, None)
