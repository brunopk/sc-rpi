"""Contains the `Version` class."""

from http import HTTPStatus
from pathlib import Path
from platform import python_version

import toml

from sc_rpi.command import Command
from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.errors import ApiError
from sc_rpi.models import responses
from sc_rpi.models.responses import Response


class Version(Command):
    """`version` command."""

    def __init__(
        self,
        command_name: str,
        config: Config,
        hw_controller: HardwareController,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, config, hw_controller)

    def validate_arguments(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command

        Raises:
            NotImplementedError: Raises this exception if the validation
                is not implemented in the child class.

        """


    def run(self) -> Response:
        """Execute the command.

        :return Response:   Returns this object with result of the execution
        """
        try:
            payload = responses.commands.Version(
                python_version(), self._get_sc_rpi_version()
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

