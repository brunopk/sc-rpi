"""Contains the `VersionCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from platform import python_version

import toml
from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.version.version_sc_rpi_result import VersionScRpiResult
from sc_rpi.commands.version.version_sc_rpi_result_payload import (
    VersionScRpiResultPayload,
)
from sc_rpi.errors import ApiError
from sc_rpi.models.command.command import Command

# TODO: return the correct object for each MQTT topic


@dataclass
class VersionCmd(Command[None]):
    """`version` command."""

    name: str = "version"

    def run(self) -> dict[str, DataClassJSONMixin | str]:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        try:
            payload = VersionScRpiResultPayload(python_version(), self._get_sc_rpi_version())
            return VersionScRpiResult(HTTPStatus.ACCEPTED, VersionCmd.name, payload)
        except FileNotFoundError as ex:
            raise ApiError from ex
        except ApiError:
            raise
        except Exception as ex:
            raise ApiError from ex

    def _get_sc_rpi_version(self) -> str:
        sc_rpi_version = None
        toml_path = Path("pyproject.toml")
        with toml_path.open() as file:
            toml_data = toml.load(file)
            sc_rpi_version = toml_data["tool"]["poetry"]["version"]

        if sc_rpi_version is None:
            raise ApiError(message="Cannot obtain SC RPI version from .toml file")

        return sc_rpi_version

