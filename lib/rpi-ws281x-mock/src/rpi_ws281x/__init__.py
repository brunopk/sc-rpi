"""Provides a mock for classes in rpi_ws281x module."""

import logging

LOGGER = logging.getLogger(__name__)


class Color:
  def __init__(self, r, g, b):
    pass

class PixelStrip:
  def __init__(self, n, pin, freq_hz, dma, invert, brightness, channel):
    pass

  def begin(self):
    LOGGER.debug("Initializing strip")

  def setPixelColor(self, index: int, color: Color):
    pass

  def show(self) -> None:
    """Show the actual state of the strip."""
    LOGGER.debug("Changing colors")