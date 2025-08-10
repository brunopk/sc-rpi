"""Contains the `MQTTConfig` class."""

from dataclasses import dataclass

from sc_rpi.models.config.mqtt.broker import BrokerConfig
from sc_rpi.models.config.mqtt.topics import TopicConfig


@dataclass
class MQTTConfig:
  """Contains configurations for MQTT."""

  broker: BrokerConfig

  topics: TopicConfig
