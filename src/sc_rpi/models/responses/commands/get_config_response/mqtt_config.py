"""Contains `MQTTConfig` class."""

from dataclasses import dataclass


@dataclass
class MQTTConfig:
  """Contains configurations for MQTT broker."""

  homeassistant_topic: str

  host: str

  port: int
