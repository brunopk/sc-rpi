"""Contains the `GetConfig` class."""


from http import HTTPStatus

from sc_rpi.command import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.models import responses
from sc_rpi.models.internal.config import Config
from sc_rpi.models.responses import Response, ResponseOk
from sc_rpi.utils import Collector


class GetConfig(Command):
    """`get_config` command."""

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
        """Validate the arguments."""

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        strip_config = responses.config.StripConfig(
            self._config.strip_config.brightness,
            self._config.strip_config.channel,
            self._config.strip_config.dma,
            self._config.strip_config.freq_hz,
            self._config.strip_config.invert,
            self._config.strip_config.pin,
            self._config.strip_config.strip_length,
        )
        config = responses.config.Config(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.host,
            self._config.log_level,
            self._config.port,
            self._config.status_led,
            strip_config,
        )

        return ResponseOk(HTTPStatus.ACCEPTED, config)
