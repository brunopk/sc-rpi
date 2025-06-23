"""`disconnect` command."""

from http import HTTPStatus

from command import Command
from hardware_controller import HardwareController
from responses import Response, ResponseOk


class Disconnect(Command):
    """`disconnect` command."""

    CMD_NAME = "disconnect"

    def __init__(self, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(hw_controller)

    def validate_arguments(self) -> None:
        """Validate command arguments."""

    def run(self) -> Response:
        """Execute the command.

        :return Response:   Returns this object with result of the execution
        :raises ApiError:   Raises this exception when command execution fails
                            for a well-known reason.
        """
        return ResponseOk(HTTPStatus.ACCEPTED, Disconnect.CMD_NAME)
