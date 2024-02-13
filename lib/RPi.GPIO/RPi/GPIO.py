import logging

logger = logging.getLogger(__name__)

BCM = "BCM"
OUT = "OUT"
HIGH = "HIGH"
LOW = "LOW"

def setmode(mode: str):
  logger.info(f'Setting mode {mode} for GPIO')

def setwarnings(mode: bool):
  logger.info(f'Warnings {"enabled" if mode else "disabled"} for GPIO')

def setup(pin_number: int, mode: str):
  if mode != OUT:
    logger.warn(f"Trying to set GPIO PIN {pin_number} with an unknown mode: {mode}")
  logger.info(f'GPIO PIN {pin_number} set for OUT operations')

def output(pin_number: int, value: str):
  if not value.__eq__(HIGH) and not value.__eq__(LOW):
    logger.warn(f"Trying to set GPIO PIN {pin_number} in an unknown state: {value}")
  logger.info(f'GPIO PIN {pin_number} {value}')

def cleanup():
  logger.info('GPIO cleanup')