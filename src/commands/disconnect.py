"""Contains the `Disconnect` class."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models.responses import Response, ResponseOk
from utils import Collector


class Disconnect(Command):
    """`disconnect` command."""

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
        """Validate command arguments."""

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution
        :raises ApiError: Raises this exception when command execution fails
            for a well-known reason.
        """
        return ResponseOk(HTTPStatus.ACCEPTED)
