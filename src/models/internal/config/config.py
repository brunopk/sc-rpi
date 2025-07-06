"""Contains the Section class."""

from dataclasses import dataclass

from .strip import StripConfig


@dataclass
class Config:
  """Main configuration class.

  This class may encapsulate other configuration classes.
  """

  connection_timeout: float

  default_gateway: str

  default_network_interface: str

  env: str

  host: str

  log_level: str

  port: int

  status_led: int

  strip_config: StripConfig


