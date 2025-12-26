"""Contains the `State` class."""

from enum import Enum


class Schema(Enum):
    """Used for Home Assistant discovery messages."""

    JSON = "json"
