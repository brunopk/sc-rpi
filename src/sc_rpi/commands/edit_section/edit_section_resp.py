"""Contains the `EditSectionResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.models import Response, StatusResp

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class EditSectionResp(Response[StatusResp]):
    """Contains available sections."""

    payload: StatusResp

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        payload: StatusResp,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (StatusResp): The result of a command.

        """
        super().__init__(status, command_name, payload, None)
