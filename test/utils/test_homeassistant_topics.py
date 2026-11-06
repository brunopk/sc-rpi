"""Tests for the Home Assistant availability topic and discovery message."""

import json
from unittest import TestCase

from sc_rpi.enums.homeassistant import ColorMode, Schema
from sc_rpi.models.homeassistant import HAMQTTDiscoveryMessage
from sc_rpi.utils.topics import build_ha_availability_topic


class TestAvailability(TestCase):
    """Tests for availability topic."""

    def test_availability_topic(self) -> None:
        """Topic follows the documented format."""
        self.assertEqual(
            "scrpi/homeassistant/section_1/availability",
            build_ha_availability_topic("section_1"),
        )

    def test_discovery_contains_availability_topic(self) -> None:
        """The discovery JSON includes `availability_topic`."""
        message = HAMQTTDiscoveryMessage(
            "Desk",
            brightness=True,
            command_topic="c",
            object_id="section_1",
            schema=Schema.JSON,
            state_topic="s",
            supported_color_modes=[ColorMode.RGB],
            unique_id="section_1",
            availability_topic=build_ha_availability_topic("section_1"),
        )
        data = json.loads(message.to_json())
        self.assertEqual(
            "scrpi/homeassistant/section_1/availability", data["availability_topic"]
        )

    def test_discovery_omits_availability_topic_when_not_set(self) -> None:
        """The field is optional."""
        message = HAMQTTDiscoveryMessage(
            "Desk",
            brightness=True,
            command_topic="c",
            object_id="x",
            state_topic="s",
            unique_id="x",
        )
        self.assertNotIn("availability_topic", json.loads(message.to_json()))
