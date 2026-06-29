"""Contains MQTT configuration classes."""

from dataclasses import dataclass


@dataclass
class BrokerConfig:
  """Contains configurations for the MQTT broker."""

  host: str

  password: str

  port: int

  username: str


@dataclass
class MQTTConfig:
  """Contains MQTT configuration such as broker configuration."""

  broker_config: BrokerConfig
