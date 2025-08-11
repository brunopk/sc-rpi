"""Contains the `StripConfig` class."""

from dataclasses import dataclass

from sc_rpi.models.config.strip_config.section import Section


@dataclass
class StripConfig:
  """Contains configurations for the led strip.

  Includes :
    - Configurations for the rpi_ws281x library
    - Sections in the strip
  """

  brightness: int

  channel: int

  dma: int

  freq_hz: int

  invert: bool

  pin: int

  strip_length: int

  sections: list[Section]
