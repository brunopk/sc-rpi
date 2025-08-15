"""Contains `TopicConfig` class."""

from dataclasses import dataclass


@dataclass
class TopicsConfig:
  """Contains MQTT topics (or prefixes)."""

  ha_topic_prefix: str

  sc_rpi_topic_prefix: str
