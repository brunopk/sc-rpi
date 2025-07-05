"""`version` command."""

from http import HTTPStatus
from pathlib import Path
from platform import python_version

import toml

from command import Command
from controllers import HardwareController
from errors import ApiError
from models import responses
from models.responses import Response, ResponseOk


class Version(Command):
    """`version` command."""

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            command_name (str):Extracted from the file name by another module
                and passed in. This is the name shown to users or used to invoke
                the command.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, hw_controller)

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
        :raises ApiError:   Raises this exception when command execution fails
                            for a well-known reason.
        """
        try:
            data = responses.Version(python_version(), self._get_sc_rpi_version())
            return ResponseOk(HTTPStatus.ACCEPTED, data)
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

