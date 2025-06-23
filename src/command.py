"""Contains the `Command` class.

To implement a command:

- It must be implemented in its own module within the commands package.
- The command class must inherit from this class and be named using the 
  camelized version of the module name. For example, if the module is 
  section_add.py, the class name should be SectionAdd.

The command name for JSON representation will be generated from the module name.
"""

from hardware_controller import HardwareController
from responses import Response


class Command:
    """Represents a command that can be executed in SC RPI."""

    def __init__(self, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            hw_controller (HardwareController): Used to control the strip.

        """
        self._args: dict = {}
        self._hw_controller = hw_controller

    def set_arguments(self, args: dict) -> None:
        """Set the arguments of the command.

        Args:
            args (dict): Arguments for the command.

        """
        self._args = args

    def validate_arguments(self):
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
            Response: Returns this object with result of the execution

        Raises:
            ApiError:   Raises this exception when command execution fails
                        for a well-known reason.
            NotImplementedError:    Raises this exception if the command is
                                    not implemented in the child class.

        """
        raise NotImplementedError
