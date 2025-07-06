"""Contains the `Command` class."""

from controllers import HardwareController
from models.responses import Response
from utils import Collector


class Command:
    """Represents a command of SC RPI.

    To implement a command:

    1. Create the corresponding module in the commands package.
    2. Create the a child class of `Command` and name it with the camelized version of \
        the module name. For example, if the module is `section_add.py`, the class \
            name should be `SectionAdd`.
    3. Copy and re-implement `__init__`, `run` and `validate_arguments`.
    """

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
        self.command_name = command_name
        self.args: dict = {}
        self._hw_controller = hw_controller
        self._collector = collector

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
            ApiError:
            NotImplementedError:

        """
        raise NotImplementedError
