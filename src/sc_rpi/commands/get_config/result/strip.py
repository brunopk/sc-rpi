"""Main class: `StripConfig`."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of leds in the strip."""

    end: int

    id: str

    name: str

    start: int

@dataclass
class StripConfig:
  """Contains configurations for the rpi_ws281x library."""

  brightness: int

  channel: int

  default_section_brightness: int

  dma: int

  freq_hz: int

  invert: bool

  pin: int

  strip_length: int

  sections: list[Section]
