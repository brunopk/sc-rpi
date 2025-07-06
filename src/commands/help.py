"""Contains the `Help` class."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models import responses
from models.responses import Response, ResponseOk
from utils import Collector
from utils.commands import load_command_names


class Help(Command):
    """`help` command."""

    def __init__(
        self,
        command_name: str,
        hw_controller: HardwareController,
        collector: Collector,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            hw_controller (HardwareController): Used to control the strip.
            collector (Collector): Used to collect information of clients of SC RPI.

        """
        super().__init__(command_name, hw_controller, collector)

    def validate_arguments(self) -> None:
        """Validate the arguments."""

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        command_names = load_command_names()
        data = responses.Help(sorted(command_names))
        return ResponseOk(HTTPStatus.ACCEPTED, data)


