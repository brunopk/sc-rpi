"""Main class: `MQTTConfig`."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BrokerConfig:
  """Contains configurations for MQTT broker."""

  host: str

  port: int

@dataclass
class MQTTConfig:
  """Contains configurations for MQTT."""

  broker_config: BrokerConfig
