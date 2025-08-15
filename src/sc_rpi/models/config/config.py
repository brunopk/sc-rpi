"""Contains the Section class."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.config.mqtt_config.mqtt_config import MQTTConfig
from sc_rpi.models.config.strip_config.strip_config import StripConfig


@dataclass
class Config(DataClassJSONMixin):
  """Contains SC RPi configurations.

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
