"""`disconnect` command."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models import Response, ResponseOk


class Disconnect(Command):
    """`disconnect` command."""

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            command_name (str):Extracted from the file name by another module and
                passed in.This is the name shown to users or used to invoke the command.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, hw_controller)

    def validate_arguments(self) -> None:
        """Validate command arguments."""

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution
        :raises ApiError: Raises this exception when command execution fails
            for a well-known reason.
        """
        return ResponseOk(HTTPStatus.ACCEPTED, self._command_name)
