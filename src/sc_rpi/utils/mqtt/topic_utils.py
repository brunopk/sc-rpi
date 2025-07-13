"""Module with functions to work with the MQTT protocol."""

from __future__ import annotations

import re

HA_COMMAND_TOPIC_PATTERN = re.compile(r"^homeassistant\/light\/([^\/#\x00]+)\/set$")
SC_RPI_COMMAND_TOPIC_PATTERN = re.compile(r"^scrpi\/commands$")

def build_ha_discovery_topic(topic_prefix: str) -> str:
  """Build Home Assistant entity discovery topic \

  (see
    [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/)\
      for more information).

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").
      entity_id (str): Entity ID in Home Assistant.

  Returns:
      str: The topic name.

  """
  # As described in https://www.home-assistant.io/integrations/light.mqtt/,
  # this topic can also be defined by user and and passed in entity creation.
  return f"{topic_prefix}/config"

def build_ha_command_topic(topic_prefix: str) -> str:
  """Build Home Assistant command topic for all entities provided by SC RPi.

  (see
    [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/)\
      for more information).

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").

  Returns:
      str: The topic name.

  """
  # As described in https://www.home-assistant.io/integrations/light.mqtt/,
  # this topic can also be defined by user and and passed in entity creation.
  return f"{topic_prefix}/light/+/set"

def build_ha_entity_state_topic(topic_prefix: str, entity_id: str) -> str:
  """Build Home Assistant entity state topic \

  (see
    [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/)\
      for more information).

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").
      entity_id (str): Entity ID in Home Assistant.

  Returns:
      str: The topic name.

  """
  # As described in https://www.home-assistant.io/integrations/light.mqtt/,
  # this topic can also be defined by user and and passed in entity creation.
  return f"{topic_prefix}/{entity_id}/state"

def build_sc_rpi_command_topic(topic_prefix: str) -> str:
  """Build the SC RPi command topic.

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").

  Returns:
      str: The topic name.

  """
  return f"{topic_prefix}/commands"

def build_sc_rpi_response_topic(topic_prefix: str) -> str:
  """Build the SC RPi responses topic.

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").

  Returns:
      str: The topic name.

  """
  return f"{topic_prefix}/response"

def matches_ha_command_topic(topic: str) -> bool:
  """Indicate whether the topic matches the Home Assistant command topic \

  (see also `build_ha_command_topic`).

  Args:
      topic (str): Topic to be tested.

  Returns:
      bool: Returns a boolean indicating whether the topic matches the Home Assistant \
        command topic.

  """
  return HA_COMMAND_TOPIC_PATTERN.match(topic) is not None

def matches_sc_rpi_command_topic(topic: str) -> bool:
  """Indicate whether the topic matches the SC RPi command topic \

  (see also `build_ha_command_topic`).

  Args:
      topic (str): Topic to be tested.

  Returns:
      bool: Returns a boolean indicating whether the topic matches the SC RPi command \
        topic.

  """
  return SC_RPI_COMMAND_TOPIC_PATTERN.match(topic) is not None
