"""Contains the HAMQTTDiscoveryMessage class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.enums.homeassistant import ColorMode, Schema

# TODO: Investigate why rgb topic is not working (by the way state topic is being used so it's not an important issue)

@dataclass
class HAMQTTDiscoveryMessage(DataClassJSONMixin):
    """Used for the Home Assistant entity discovery process.

    Important :

    - Home Assistant requires `unique_id` to be unique to allow the entity to be \
      managed through the UI.
    - When schema is defined as JSON, Home Assistant will expect state, color, etc as \
      keys of a JSON object in state topic messages.
    - `rgb` attribute cannot be set when `supported_color_modes` contains \
      `ColorMode.RGB` (see Home Assistant error logs).
    - `rgb_state_topic` is optional (RGB color is sent in state_topic)

    More information:
      - [MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery): \
        describes the discovery process in general.
      - [MQTT Light](https://www.home-assistant.io/integrations/light.mqtt/): \
        describes the format and attributes to configure light entities.

    """

    class Config:
      """Required by Mashumaro library."""

      omit_none = True

    name: str

    brightness: bool

    command_topic: str

    object_id: str

    state_topic: str

    unique_id: str

    rgb: Optional[bool] = None

    rgb_state_topic: Optional[str] = None

    schema: Optional[Schema] = None

    supported_color_modes: Optional[list[ColorMode]] = None
