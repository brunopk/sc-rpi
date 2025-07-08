"""Contains the `Help` class."""

from http import HTTPStatus

from sc_rpi.command import Command
from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.models import responses
from sc_rpi.models.responses import Response, ResponseOk
from sc_rpi.utils.commands import command_utils


class Help(Command):
    """`help` command."""

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
            collector (Collector): Used to collect information of clients of SC RPI.

        """
        super().__init__(command_name, config, hw_controller)

    def validate_arguments(self) -> None:
        """Validate the arguments."""

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        command_names = command_utils.load_command_names()
        data = responses.Help(sorted(command_names))
        return ResponseOk(HTTPStatus.ACCEPTED, data)


