"""Contains the `Version` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from platform import python_version

import toml

from sc_rpi.errors import ApiError
from sc_rpi.models import responses
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response


@dataclass
class Version(Command[None]):
    """`version` command."""

    name: str = "version"

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        try:
            payload = responses.commands.Version(
                python_version(),
                self._get_sc_rpi_version(),
            )
            return Response(HTTPStatus.ACCEPTED, payload)
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

