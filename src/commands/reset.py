"""Contains the `Reset` class."""

from http import HTTPStatus

from command import Command
from controllers import HardwareController
from models.internal.config import Config
from models.responses import Response, ResponseOk
from utils import Collector


class Reset(Command):
    """`reset` command."""

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
        """Validate command arguments."""

    def run(self) -> Response:
        """Execute the command.

        :return Response:   Returns this object with result of the execution
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()
        return ResponseOk(HTTPStatus.ACCEPTED)
