"""Contains the `Command` class."""

from controllers import HardwareController
from models.responses import Response


class Command:
    """Represents a command that can be executed in SC RPI.

    See `src/commands/__init__.py`.
    """

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command (constructor).

        Args:
            command_name (str): Extracted from the file name by another module and
                passed in. This is the name shown to users or used to invoke the
                command.
            hw_controller (HardwareController): Used to control the strip.

        """
        self.command_name = command_name
        self.args: dict = {}
        self._hw_controller = hw_controller

    def validate_arguments(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command

        Raises:
            NotImplementedError: Raises this exception if the validation
                is not implemented in the child class.

        """
        raise NotImplementedError

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        Raises:
            ApiError: Raises this exception when command execution fails
                for a well-known reason.
            NotImplementedError: Raises this exception if the command is
                not implemented in the child class.

        """
        raise NotImplementedError
