"""Contains the result classes for the `version` command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.results import Result

if TYPE_CHECKING:
    from http import HTTPStatus


@dataclass
class VersionResultPayload(DataClassJSONMixin):
    """Includes different version numbers, such as the SC RPI version."""

    python_version: str

    sc_rpi_version: str


@dataclass
class VersionResult(Result[VersionResultPayload]):
    """Result for the `version` command."""

    payload: VersionResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: VersionResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (VersionResultPayload): The result of the command.

        """
        super().__init__(status_code, command_name, payload, None)
