"""Contains `StripConfig` class."""

from dataclasses import dataclass

from sc_rpi.models.commands.all.get_config.strip_config.section import Section


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

  sections: list[Section]
