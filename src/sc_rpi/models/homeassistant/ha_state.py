"""Contains the `Command` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.enums.homeassistant import State
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.models.color import Color


@dataclass
class HAState(DataClassJSONMixin):
    """Model to send messages for the [sate topic](https://www.home-assistant.io/integrations/light.mqtt/#state_topic)."""

    class Config:
      """Required by Mashumaro library."""

      omit_none = True

    state: State

    brightness: Optional[int]

    color: Optional[Color] = None

    color_mode: Optional[ColorMode] = None




