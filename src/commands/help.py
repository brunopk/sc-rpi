"""Contains the `Help` class."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models import responses
from models.responses import Response, ResponseOk
from utils.commands import load_command_names


class Help(Command):
    """`help` command."""

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command (constructor).

        Args:
            command_name (str):Extracted from the file name by another module
                and passed in. This is the name shown to users or used to invoke
                the command.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, hw_controller)

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


