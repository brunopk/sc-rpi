"""Enums used for Home Assistant MQTT messages."""

from enum import Enum


class ColorMode(Enum):
    """Used for Home Assistant commands."""

    RGB = "rgb"

class Schema(Enum):
    """Used for Home Assistant discovery messages."""

    JSON = "json"

class State(Enum):
    """Used for Home Assistant commands."""

    ON = "ON"

    OFF = "OFF"
