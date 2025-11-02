"""Contains the `Command` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.enums.homeassistant import State
from sc_rpi.models.homeassistant.color import Color


@dataclass
class HACommand(DataClassJSONMixin):
    """Model to receive messages in the [commands_topic](https://www.home-assistant.io/integrations/light.mqtt/#command_topic).

    Important:
    - Optional attributes (typed as `Optional[...]`), must have a default value.
    - Ignore Ruff warnings about `Optional` as using `|` instead of `Optional` makes \
      `from_dict` raise exceptions.

    """

    state: State

    brightness: Optional[int] = None

    color: Optional[Color] = None

