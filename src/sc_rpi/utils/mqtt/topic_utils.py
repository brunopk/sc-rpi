"""Module with functions to work with the MQTT protocol."""

from __future__ import annotations

import re

HA_COMMAND_TOPIC_PATTERN = re.compile(r"^homeassistant\/light\/([^\/#\x00]+)\/set$")
SC_RPI_COMMAND_TOPIC_PATTERN = re.compile(r"^scrpi\/commands$")

def build_ha_discovery_topic(object_id: str) -> str:
  """Build Home Assistant entity discovery topic.

  More information in :
  - [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/).
  - [MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)

  Args:
      object_id (str): As described in HA documentation, the <object_id> part of the \
        topic may not match with entity ID, it's just used to structure other topics.

  Returns:
      str: The topic name.

  """
  return f"homeassistant/light/{object_id}/config"

def build_ha_command_topic(object_id: str = "+") -> str:
  """Build Home Assistant command topic for all entities provided by SC RPi.

  More information in [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt).

  Args:
      object_id (str | None, optional): Object to which send the commands (this is \
        defined with [discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery).
        If it's not defined, it will return command topic used for subscriptions (with \
          the `+` wildcard to consume messages from different entities). Defaults to \
            `+`.

  Returns:
      str: The topic name.

  """
  return f"homeassistant/light/{object_id}/set"

def build_ha_state_topic(object_id: str) -> str:
  """Build Home Assistant entity state topic \

   More information in [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt).

  Args:
      object_id (str): Object to which send the commands (this is defined with \
        [discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)
      entity_id (str): Entity ID in Home Assistant.

  Returns:
      str: The topic name.

  """
  return f"homeassistant/light/{object_id}/state"

def build_sc_rpi_command_topic() -> str:
  """Build the SC RPi command topic.

  Args:
      topic_prefix (str): First part of the topic name (do not include the last "/").

  Returns:
      str: The topic name.

  """
  return "sc_rpi/commands"

def build_sc_rpi_response_topic() -> str:
  """Build the SC RPi responses topic.

  Returns:
      str: The topic name.

  """
  return "scrpi/response"

def matches_ha_command_topic(topic: str) -> bool:
  """Indicate whether the topic matches the Home Assistant command topic \

  See also `build_ha_command_topic`.

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
