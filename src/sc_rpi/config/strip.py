"""Contains `PixelStrip` class."""

from dataclasses import dataclass


@dataclass
class StripConfig:
  """Contains configurations for the rpi_ws281x library."""

  brightness: int

  channel: int

  dma: int

  freq_hz: int

  invert: bool

  pin: int

  strip_length: int
