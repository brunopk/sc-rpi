"""Helpers to build the messages that keep Home Assistant entities up to date."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sc_rpi.enums.homeassistant import ColorMode, Schema, State
from sc_rpi.models import Color
from sc_rpi.models.homeassistant import HAAvailability, HAMQTTDiscoveryMessage, HAState
from sc_rpi.utils.topics import (
    SC_RPI_STATUS_TOPIC,
    build_ha_availability_topic,
    build_ha_command_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
)

if TYPE_CHECKING:
    from mashumaro.mixins.json import DataClassJSONMixin

    from sc_rpi.models import SectionInternalRepresentation

AVAILABLE = "online"
"""Payload that marks an entity as available (Home Assistant default)."""

UNAVAILABLE = "offline"
"""Payload that marks an entity as unavailable (Home Assistant default)."""


def build_ha_refresh_messages(
    previous_sections: list[SectionInternalRepresentation],
    new_sections: list[SectionInternalRepresentation],
    brightness: int,
) -> dict[str, DataClassJSONMixin | str]:
    """Build the messages that replace the published entities with `new_sections`.

    The dict's insertion order is the order in which the messages must be published
    (Python dicts keep insertion order), so each entity exists and is available before
    its state arrives:

          1. `offline` for each previous section whose id is not in `new_sections`.
          2. Discovery for each new section (with the cross availability).
          3. `online` for each new section.
          4. State for each new section (ON/OFF, color and brightness).

    ------------------------------------------------------------------------------------

    A section present in both lists gets no `offline` message, as a topic can appear
    only once in the dict and `online` must win. Without this rule (previous
    `[kept, old]`, new `[kept]`, `offline` sent for all previous sections)::

        messages["kept/availability"] = "offline"
        messages["old/availability"] = "offline"
        messages["kept/discovery"] = <discovery>
        messages["kept/availability"] = "online"  # keeps its first position
        messages["kept/state"] = <state>

    The dict ends in this order::

        kept/availability: online  (before the discovery)
        old/availability: offline
        kept/discovery
        kept/state

    So the `offline` of `kept` is lost and `online` is published before the discovery
    message.

    Args:
        previous_sections (list[SectionInternalRepresentation]): Sections published
            before (empty at startup).
        new_sections (list[SectionInternalRepresentation]): Sections to publish.
        brightness (int): Brightness sent in every state (default section brightness).

    Returns:
        dict: Topic -> payload.

    """
    messages: dict[str, DataClassJSONMixin | str] = {}
    new_ids = {section.id for section in new_sections}

    for section in previous_sections:
        if section.id not in new_ids:
            messages[build_ha_availability_topic(section.id)] = UNAVAILABLE

    for section in new_sections:
        # HA requires unique_id to be unique to allow managing the entity in the UI
        # TODO: add retain=True (this is just for testing)
        messages[build_ha_discovery_topic(section.id)] = HAMQTTDiscoveryMessage(
            section.name,
            availability=[
                HAAvailability(SC_RPI_STATUS_TOPIC),
                HAAvailability(build_ha_availability_topic(section.id)),
            ],
            availability_mode="all",
            brightness=True,
            command_topic=build_ha_command_topic(section.id),
            object_id=section.id,
            schema=Schema.JSON,
            state_topic=build_ha_state_topic(section.id),
            supported_color_modes=[ColorMode.RGB],
            unique_id=section.id,
        )

    for section in new_sections:
        messages[build_ha_availability_topic(section.id)] = AVAILABLE

    for section in new_sections:
        messages[build_ha_state_topic(section.id)] = HAState(
            State.ON if section.is_on else State.OFF,
            brightness=brightness,
            color=Color(*section.color_list[0]),
            color_mode=ColorMode.RGB,
        )

    return messages
