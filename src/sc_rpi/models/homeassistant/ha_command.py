"""Contains the `Command` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.homeassistant.color import Color


@dataclass
class HACommand(DataClassJSONMixin):
    """Model for the [commands_topic](https://www.home-assistant.io/integrations/light.mqtt/#command_topic).

    Using `|` instead of `Optional` makes `from_dict` raise exceptions, \
        also nested types cannot be imported with:

    ```
    if TYPE_CHECKING:
      ...
    ```
    """

    state: str

    brightness: Optional[int]

    color: Optional[Color]
