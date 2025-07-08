"""Contains the `Status` class."""

from http import HTTPStatus

from sc_rpi.command import Command
from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.models import responses
from sc_rpi.models.responses import Response, ResponseOk
from sc_rpi.utils import map_sections


class Status(Command):
    """`status` command."""

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

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._hw_controller.list_sections()
        sections = self._hw_controller.list_sections()
        data = responses.commands.Status(map_sections(sections))
        return ResponseOk(HTTPStatus.ACCEPTED, data)
