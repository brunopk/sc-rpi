"""Contains `BrokerConfig` class."""

from dataclasses import dataclass


@dataclass
class BrokerConfig:
  """Contains configurations for MQTT broker."""

  host: str

  password: str

  port: int

  username: str
