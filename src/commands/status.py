"""Contains the `Status` class."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models.internal.config import Config
from models.responses import Response, ResponseOk, commands
from utils import Collector


class Status(Command):
    """`status` command."""

    def __init__(
        self,
        command_name: str,
        config: Config,
        hw_controller: HardwareController,
        collector: Collector,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.
            collector (Collector): Used to collect information of clients of SC RPI.

        """
        super().__init__(command_name, config, hw_controller, collector)

    def validate_arguments(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command

        Raises:
            NotImplementedError: Raises this exception if the validation
                is not implemented in the child class.

        """

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._hw_controller.list_sections()
        clients = self._collector.get_clients()
        status = commands.Status(sections, clients)
        return ResponseOk(HTTPStatus.ACCEPTED, status)


