"""Contains the `GetConfigCommand` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.get_config.result import GetConfigResult, GetConfigResultPayload
from sc_rpi.commands.get_config.result.mqtt import BrokerConfig, MQTTConfig
from sc_rpi.commands.get_config.result.strip import Section, StripConfig
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC

# TODO: avoid duplicating models for configurations,this command should be able to return models in src.sc_rpi.config, maybe masking/hidding some configurations

if TYPE_CHECKING:
    from sc_rpi.models.config import strip as strip_config


def _map_sections(sections: list[strip_config.Section]) -> list[Section]:
    return [
        Section(
            section.end,
            section.id,
            section.name,
            section.start,
        )
        for section in sections
    ]


@dataclass
class GetConfig(Command[None]):
    """`get_config` command."""

    command_name: str = "get_config"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sc_rpi_result = self._map_config()
        return {SC_RPI_RESULT_TOPIC: sc_rpi_result}

    def _map_config(self) -> GetConfigResult:
        """Map the domain config to an instance of `GetConfigResult`."""
        sections = _map_sections(self._config.strip.sections)
        strip_config = StripConfig(
            self._config.strip.brightness,
            self._config.strip.channel,
            self._config.strip.dma,
            self._config.strip.freq_hz,
            self._config.strip.invert,
            self._config.strip.pin,
            self._config.strip.strip_length,
            sections,
        )

        mqtt_broker_config = BrokerConfig(
            self._config.mqtt.broker_config.host,
            self._config.mqtt.broker_config.port,
        )
        mqtt_config = MQTTConfig(mqtt_broker_config)

        payload = GetConfigResultPayload(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.log_level,
            mqtt_config,
            self._config.status_led,
            strip_config,
        )
        return GetConfigResult(
            HTTPStatus.ACCEPTED,
            self.command_name,
            payload,
        )
