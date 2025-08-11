"""Contains the `GetConfigResponse` class."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.responses.commands.get_config.mqtt import MQTTConfig
from sc_rpi.models.responses.commands.get_config.strip_config import (
  StripConfig,
)


@dataclass
class GetConfig(DataClassJSONMixin):
  """Main configuration class.

  This class may encapsulate other configuration classes.
  """

  connection_timeout: float

  default_gateway: str

  default_network_interface: str

  env: str

  log_level: str

  mqtt: MQTTConfig

  status_led: int

  strip_config: StripConfig


