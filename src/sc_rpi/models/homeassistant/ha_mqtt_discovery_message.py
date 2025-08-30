"""Contains the HAMQTTDiscoveryMessage class."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class HAMQTTDiscoveryMessage(DataClassJSONMixin):
    """Used for the Home Assistant entity discovery process.

    More information:
      - [MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery): \
        describes the discovery process in general.
      - [MQTT Light](https://www.home-assistant.io/integrations/light.mqtt/): \
        describes the format and attributes to configure light entities.

    """

    name: str

    brightness: bool

    command_topic: str

    rgb: bool

    schema: str

    state_topic: str

    unique_id: str
