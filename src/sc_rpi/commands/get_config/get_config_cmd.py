"""Contains the `GetConfigCommand` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.get_config.get_config_resp import (
    BrokerConfig,
    GetConfigResp,
    MQTTConfig,
    StripConfig,
    TopicsConfig,
    Section
)
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response

if TYPE_CHECKING:
    from sc_rpi.models.config import strip_config


@dataclass
class GetConfigCmd(Command[None]):
    """`get_config` command."""

    name: str = "get_config"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> Response:
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
        mqtt_topics = TopicsConfig(
            self._config.mqtt_config.topics_config.ha_topic_prefix,
            self._config.mqtt_config.topics_config.sc_rpi_topic_prefix,
        )
        mqtt_config = MQTTConfig(
            mqtt_broker_config,
            mqtt_topics,
        )


        resp = GetConfigResp(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.log_level,
            mqtt_config,
            self._config.status_led,
            strip_config,
        )

        # TODO: CONTINUE
        # TODO: all commands should return the command name (add command name as attribute of Response)
        # TODO: all commands should have its models in his own command package (src/sc_rpi/commands/*)
        return Response(HTTPStatus.ACCEPTED, GetConfigCmd.name, resp)

    def _map_sections(self, sections: list[strip_config.Section]) -> list[Section]:
        return [
            Section(
                section.ha_entity_id,
                section.start,
                section.end,
            )
            for section in sections
        ]
