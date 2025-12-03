"""Contains the `Color` class."""

from dataclasses import dataclass


@dataclass
class Color:
    """Define colors (RGB)."""

    r: int

    g: int

    b: int
