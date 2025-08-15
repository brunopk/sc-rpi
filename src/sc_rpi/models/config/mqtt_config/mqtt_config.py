"""Contains the `MQTTConfig` class."""

from dataclasses import dataclass

from sc_rpi.models.config.mqtt_config.broker_config import BrokerConfig
from sc_rpi.models.config.mqtt_config.topics_config import TopicsConfig


@dataclass
class MQTTConfig:
  """Contains configurations for MQTT."""

  broker_config: BrokerConfig

  topics_config: TopicsConfig
