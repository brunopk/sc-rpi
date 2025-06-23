"""`status` command."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models import Response, ResponseOk


class Status(Command):
    """`status` command."""

    CMD_NAME = "status"

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

        :return Response: Returns this object with result of the execution.
        :raises ApiError: Raises this error when command execution fails for
                          a well-known reason.
        """
        status = self._hw_controller.status()
        return ResponseOk(HTTPStatus.OK, Status.CMD_NAME, payload=status)
