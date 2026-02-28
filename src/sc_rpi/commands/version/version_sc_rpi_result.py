"""Contains the `VersionResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sc_rpi.commands.available.version.version_sc_rpi_result_payload import (
  VersionScRpiResultPayload,
)
from sc_rpi.commands.sc_rpi_base_result import ScRpiBaseResult

if TYPE_CHECKING:
  from http import HTTPStatus

# TODO: add python version

@dataclass
class VersionScRpiResult(ScRpiBaseResult[VersionScRpiResultPayload]):
    """Contains available sections."""

    payload: VersionScRpiResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        version_sc_rpi_result_payload: VersionScRpiResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            version_sc_rpi_result_payload (VersionScRpiResultPayload): The result of a \
                command.

        """
        super().__init__(status_code, command_name, version_sc_rpi_result_payload, None)
