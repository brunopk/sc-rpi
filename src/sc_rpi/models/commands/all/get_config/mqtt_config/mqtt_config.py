"""Contains the `MQTTConfig` class."""

from dataclasses import dataclass

from sc_rpi.models.commands.all.get_config.mqtt_config.broker_config import BrokerConfig


@dataclass
class MQTTConfig:
  """Contains configurations for MQTT."""

  broker_config: BrokerConfig
