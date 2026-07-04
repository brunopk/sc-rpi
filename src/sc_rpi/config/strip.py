"""Contains LED strip configuration classes."""

from dataclasses import dataclass

from sc_rpi.models import Color


@dataclass
class Section:
  """Represents a section of leds in the strip."""

  color: Color

  end: int

  id: str

  is_on: bool

  name: str

  start: int


@dataclass
class StripConfig:
  """Contains configurations for the led strip.

  Includes :
    - Configurations for the rpi_ws281x library
    - Sections in the strip
  """

  brightness: int

  channel: int

  default_section_brightness: int

  dma: int

  freq_hz: int

  invert: bool

  pin: int

  strip_length: int

  sections: list[Section]
