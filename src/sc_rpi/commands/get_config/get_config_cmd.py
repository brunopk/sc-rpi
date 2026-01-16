"""Contains the `GetConfigCommand` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.get_config.get_config_sc_rpi_result import GetConfigScRpiResult
from sc_rpi.commands.get_config.get_config_sc_rpi_result_payload import (
    GetConfigScRpiResultPayload,
)
from sc_rpi.commands.get_config.mqtt_config.broker_config import BrokerConfig
from sc_rpi.commands.get_config.mqtt_config.mqtt_config import MQTTConfig
from sc_rpi.commands.get_config.strip_config.section import Section
from sc_rpi.commands.get_config.strip_config.strip_config import StripConfig
from sc_rpi.models.command.command import Command, CommandResult
from sc_rpi.utils.commands.decorators import log_call

if TYPE_CHECKING:
    from sc_rpi.models.config import strip_config


# TODO: CONTINUE return the correct object for each MQTT topic

@dataclass
class GetConfigCmd(Command[None]):
    """`get_config` command."""

    name: str = "get_config"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._map_sections(self._config.strip_config.sections)
        strip_config = StripConfig(
            self._config.strip_config.brightness,
            self._config.strip_config.channel,
            self._config.strip_config.dma,
            self._config.strip_config.freq_hz,
            self._config.strip_config.invert,
            self._config.strip_config.pin,
            self._config.strip_config.strip_length,
            sections,
        )


        mqtt_broker_config = BrokerConfig(
            self._config.mqtt_config.broker_config.host,
            self._config.mqtt_config.broker_config.port,
        )
        mqtt_config = MQTTConfig(mqtt_broker_config)


        payload = GetConfigScRpiResultPayload(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.log_level,
            mqtt_config,
            self._config.status_led,
            strip_config,
        )

        return GetConfigScRpiResult(HTTPStatus.ACCEPTED, GetConfigCmd.name, payload)

    def _map_sections(self, sections: list[strip_config.Section]) -> list[Section]:
        return [
            Section(
                section.end,
                section.id,
                section.name,
                section.start,
            )
            for section in sections
        ]
