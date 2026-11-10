"""Tests for the Home Assistant availability topics and discovery message."""

import json
from unittest import TestCase

from sc_rpi.enums.homeassistant import ColorMode, Schema
from sc_rpi.models.homeassistant import HAAvailability, HAMQTTDiscoveryMessage
from sc_rpi.utils.topics import SC_RPI_AVAILABILITY_TOPIC, build_ha_availability_topic


class TestAvailability(TestCase):
    """Tests for availability topics."""

    def test_availability_topic(self) -> None:
        """Topic follows the documented format."""
        self.assertEqual(
            "scrpi/homeassistant/section_1/availability",
            build_ha_availability_topic("section_1"),
        )

    def test_discovery_contains_cross_availability(self) -> None:
        """The discovery JSON has both topics (global first) and mode `all`."""
        message = HAMQTTDiscoveryMessage(
            "Desk",
            brightness=True,
            command_topic="c",
            object_id="section_1",
            schema=Schema.JSON,
            state_topic="s",
            supported_color_modes=[ColorMode.RGB],
            unique_id="section_1",
            availability=[
                HAAvailability(SC_RPI_AVAILABILITY_TOPIC),
                HAAvailability(build_ha_availability_topic("section_1")),
            ],
            availability_mode="all",
        )
        data = json.loads(message.to_json())
        self.assertEqual("all", data["availability_mode"])
        self.assertEqual(
            [
                {"topic": "scrpi/availability"},
                {"topic": "scrpi/homeassistant/section_1/availability"},
            ],
            data["availability"],
        )
        self.assertNotIn("availability_topic", data)

    def test_discovery_omits_availability_when_not_set(self) -> None:
        """The fields are optional."""
        message = HAMQTTDiscoveryMessage(
            "Desk",
            brightness=True,
            command_topic="c",
            object_id="x",
            state_topic="s",
            unique_id="x",
        )
        data = json.loads(message.to_json())
        self.assertNotIn("availability", data)
        self.assertNotIn("availability_mode", data)

    def test_status_topic(self) -> None:
        """The global topic has the documented value."""
        self.assertEqual("scrpi/availability", SC_RPI_AVAILABILITY_TOPIC)
