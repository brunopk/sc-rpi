import logging

_logger = logging.getLogger(__name__)


class Color:
  def __init__(self, r, g, b):
    pass

class PixelStrip:
  def __init__(self, n, pin, freq_hz, dma, invert, brightness, channel):
    pass

  def begin(self):
    _logger.info('Initializing strip ...')
  
  def setPixelColor(self, index: int, color: Color):
    pass

  def show(self):
    _logger.info('Displaying light colors ...')
