"""Contains the `EditSectionResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.get_config.get_config_resp.config import Config
from sc_rpi.models import Response

if TYPE_CHECKING:
  from http import HTTPStatus

# TODO: create a response object for all commands

@dataclass
class GetConfigResp(Response[Config]):
  """Contains available sections."""

  payload: Config

  def __init__(self, status: HTTPStatus, command_name: str, payload: Config) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (Config): The result of a command.

        """
        super().__init__(status, command_name, payload, None)
