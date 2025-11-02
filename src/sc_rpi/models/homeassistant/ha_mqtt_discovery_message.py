"""Contains the HAMQTTDiscoveryMessage class."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class HAMQTTDiscoveryMessage(DataClassJSONMixin):
    """Used for the Home Assistant entity discovery process.

    Important :

    - Home Assistant requires `unique_id` to be unique to allow the entity to be \
      managed through the UI.
    - `object_id` is used as part of an entity's command topic name.

    More information:
      - [MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery): \
        describes the discovery process in general.
      - [MQTT Light](https://www.home-assistant.io/integrations/light.mqtt/): \
        describes the format and attributes to configure light entities.

    """

    name: str

    brightness: bool

    command_topic: str

    object_id: str

    rgb: bool

    schema: str

    state_topic: str

    unique_id: str
