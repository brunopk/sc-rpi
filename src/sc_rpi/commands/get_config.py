"""Contains the `GetConfig` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.models import responses
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response

if TYPE_CHECKING:
    from sc_rpi.models.config import strip_config


@dataclass
class GetConfig(Command[None]):
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
        strip_config = responses.commands.get_config.strip_config.StripConfig(
            self._config.strip_config.brightness,
            self._config.strip_config.channel,
            self._config.strip_config.dma,
            self._config.strip_config.freq_hz,
            self._config.strip_config.invert,
            self._config.strip_config.pin,
            self._config.strip_config.strip_length,
            sections,
        )


        mqtt_broker_config = responses.commands.get_config.mqtt.BrokerConfig(
            self._config.mqtt.broker.host,
            self._config.mqtt.broker.port,
        )
        mqtt_topics = responses.commands.get_config.mqtt.TopicConfig(
            self._config.mqtt.topics.ha_topic_prefix,
            self._config.mqtt.topics.sc_rpi_topic_prefix,
        )
        mqtt_config = responses.commands.get_config.mqtt.MQTTConfig(
            mqtt_broker_config,
            mqtt_topics,
        )


        config = responses.commands.get_config.GetConfig(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.log_level,
            mqtt_config,
            self._config.status_led,
            strip_config,
        )

        return Response(HTTPStatus.ACCEPTED, config)

    def _map_sections(
        self,
        sections: list[strip_config.Section],
    ) -> list[responses.commands.get_config.strip_config.Section]:
        return [
            responses.commands.get_config.strip_config.Section(
                section.ha_entity_id,
                section.start,
                section.end,
            )
            for section in sections
        ]
