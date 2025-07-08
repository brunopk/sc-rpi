"""Contains the `Reset` class."""

from http import HTTPStatus

from sc_rpi.command import Command
from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response


class Reset(Command):
    """`reset` command."""

    def __init__(
        self,
        command_name: str,
        config: Config,
        hw_controller: HardwareController,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, config, hw_controller)

    def validate_arguments(self) -> None:
        """Validate command arguments."""

    def run(self) -> Response:
        """Execute the command.

        :return Response:   Returns this object with result of the execution
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()
        return Response(HTTPStatus.ACCEPTED)
