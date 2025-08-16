"""Contains the `GetConfigCommand` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.get_config.get_config_resp.config import Config
from sc_rpi.commands.get_config.get_config_resp.get_config_resp import GetConfigResp
from sc_rpi.commands.get_config.get_config_resp.mqtt_config.broker_config import (
    BrokerConfig,
)
from sc_rpi.commands.get_config.get_config_resp.mqtt_config.mqtt_config import (
    MQTTConfig,
)
from sc_rpi.commands.get_config.get_config_resp.mqtt_config.topics_config import (
    TopicsConfig,
)
from sc_rpi.commands.get_config.get_config_resp.strip_config.section import (
    Section,
)
from sc_rpi.commands.get_config.get_config_resp.strip_config.strip_config import (
    StripConfig,
)
from sc_rpi.models.command import Command

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

    def run(self) -> GetConfigResp:
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


        payload = Config(
            self._config.connection_timeout,
            self._config.default_gateway,
            self._config.default_network_interface,
            self._config.env,
            self._config.log_level,
            mqtt_config,
            self._config.status_led,
            strip_config,
        )

        return GetConfigResp(HTTPStatus.ACCEPTED, GetConfigCmd.name, payload)

    def _map_sections(self, sections: list[strip_config.Section]) -> list[Section]:
        return [
            Section(
                section.ha_entity_id,
                section.start,
                section.end,
            )
            for section in sections
        ]
