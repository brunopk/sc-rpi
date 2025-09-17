"""Contains the `State` class."""

from enum import Enum


class State(Enum):
    """Used for Home Assistant commands."""

    ON = "ON"

    OFF = "OFF"
