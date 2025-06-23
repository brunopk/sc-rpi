"""`reset` command."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models import Response, ResponseOk


class Reset(Command):
    """`reset` command."""

    CMD_NAME = "reset"

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
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()
        return ResponseOk(HTTPStatus.ACCEPTED, Reset.CMD_NAME)
