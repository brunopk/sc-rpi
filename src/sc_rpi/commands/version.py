"""Contains the `Version` class."""

from __future__ import annotations

from http import HTTPStatus
from pathlib import Path
from platform import python_version
from typing import Any

import toml

from sc_rpi.command import Command
from sc_rpi.errors import ApiError
from sc_rpi.models import responses
from sc_rpi.models.responses import Response


class Version(Command):
    """`version` command."""

    def __init__(self, command_arguments: dict | None, **kwargs: Any) -> None:
        """Initialize the instance (constructor).

        Args:
            command_arguments (dict | None): Command arguments (defined by user).
            kwargs (Any): Arguments as defined in `Command` (`config`, \
                `hw_controller`, etc).

        """
        super().__init__(command_arguments, **kwargs)

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

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def _get_sc_rpi_version(self) -> str:
        sc_rpi_version = None
        toml_path = Path("pyproject.toml")
        with toml_path.open() as file:
            toml_data = toml.load(file)
            sc_rpi_version = toml_data["tool"]["poetry"]["version"]

        if sc_rpi_version is None:
            raise ApiError(message="Cannot obtain SC RPI version from .toml file")

        return sc_rpi_version

