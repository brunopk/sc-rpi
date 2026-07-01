"""Module with functions to work with the MQTT protocol."""

from __future__ import annotations

import re

from sc_rpi.errors.api_error import ApiError

""""
This regexp SHOULD use the same prefix defined in HA_TOPIC_PREFIX.
See also HA_TOPIC_PREFIX.
"""
HA_COMMAND_TOPIC_PATTERN = re.compile(r"^scrpi\/homeassistant\/([^\/#\x00]+)/command$")

"""
Prefix used for special topics (for example state topic) set on the discovery message.
It's the prefix for HA_COMMAND_TOPIC_PATTERN
"""
HA_TOPIC_PREFIX = "scrpi/homeassistant"

SC_RPI_COMMAND_TOPIC = "scrpi/command"

SC_RPI_RESULT_TOPIC = "scrpi/result"

def build_ha_discovery_topic(object_id: str) -> str:
  """Build Home Assistant entity discovery topic.

  More information in :
  - [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/).
  - [MQTT Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)

  Args:
      object_id (str): As described in HA documentation, the object ID is part of the \
        topic may not match with entity ID, it's just used to structure other topics.

  Returns:
      str: The topic name.

  """
  return f"homeassistant/light/{object_id}/config"

def build_ha_command_topic(object_id: str = "+") -> str:
  """Build Home Assistant command topic.

  More information in [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt).

  Args:
      object_id (str | None, optional): As described in HA documentation, the object \
        ID is part of the topic may not match with entity ID, it's just used to \
          structure other topics. Defaults to `+` to consume messages from different \
            entities.

  Returns:
      str: The topic name.

  """
  # This should match with HA_COMMAND_TOPIC_PATTERN
  return f"{HA_TOPIC_PREFIX}/{object_id}/command"

def build_ha_state_topic(object_id: str) -> str:
  """Build topic to receive state updates \

   More information in [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt).

  Args:
      object_id (str): Use the entity ID. However, HA documentation explains that \
        object ID is part of the topic may not match with entity ID, it's just used to \
        structure other topics.

  Returns:
      str: The topic name.

  """
  return f"{HA_TOPIC_PREFIX}/{object_id}/state"

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
  return topic == SC_RPI_COMMAND_TOPIC or topic == SC_RPI_COMMAND_TOPIC + "/"

def get_object_id_from_ha_command_topic(topic: str) -> str:
  """Extract object ID from topic.

  Args:
      topic (str): Topic from which to extract object ID. As described in HA \
        documentation, the object ID is part of the topic may not match with entity \
          ID, it's just used to structure other topics.

  Raises:
      ApiError:

  Returns:
      str: Extracted object ID

  """
  match = HA_COMMAND_TOPIC_PATTERN.match(topic)
  if match is None:
    raise ApiError(message=f"Cannot extract object_id from topic {topic}")
  return match.groups()[0]
