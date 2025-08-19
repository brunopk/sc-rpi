"""Contains the `VersionResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.version.version_resp_payload import VersionRespPayload
from sc_rpi.models import Response

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class VersionResp(Response[VersionRespPayload]):
    """Contains available sections."""

    payload: VersionRespPayload

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        payload: VersionRespPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (VersionRespPayload): The result of a command.

        """
        super().__init__(status, command_name, payload, None)
