"""Contains the Section class."""

from dataclasses import dataclass

from sc_rpi.config.mqtt_config import MQTTConfig
from sc_rpi.config.strip_config import StripConfig


@dataclass
class Config:
  """Main configuration class.

  This class may encapsulate other configuration classes.
  """

  connection_timeout: float

  default_gateway: str

  default_network_interface: str

  env: str

  log_level: str

  mqtt_config: MQTTConfig

  status_led: int

  strip_config: StripConfig


