"""Contains the `VersionCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from platform import python_version

import toml

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.version.result import VersionResult, VersionResultPayload
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC


@dataclass
class VersionCmd(Command[None]):
    """`version` command."""

    command_name: str = "version"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        try:
            payload = VersionResultPayload(
                python_version(),
                self._get_sc_rpi_version(),
            )
            sc_rpi_result = VersionResult(
                HTTPStatus.ACCEPTED,
                self.command_name,
                payload,
            )
        except FileNotFoundError as ex:
            raise ApiError from ex
        except ApiError:
            raise
        except Exception as ex:
            raise ApiError from ex

        return {SC_RPI_RESULT_TOPIC: sc_rpi_result}

    def _get_sc_rpi_version(self) -> str:
        sc_rpi_version = None
        toml_path = Path("pyproject.toml")
        with toml_path.open() as file:
            toml_data = toml.load(file)
            sc_rpi_version = toml_data["project"]["version"]

        if sc_rpi_version is None:
            raise ApiError(message="Cannot obtain SC RPI version from .toml file")

        return sc_rpi_version

