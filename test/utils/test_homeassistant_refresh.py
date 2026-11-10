"""Tests for `build_ha_refresh_messages`."""

from __future__ import annotations

import json
from unittest import TestCase

from sc_rpi.models import SectionInternalRepresentation
from sc_rpi.utils.homeassistant import build_ha_refresh_messages
from sc_rpi.utils.topics import (
    build_ha_availability_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
)


def _section(
    section_id: str,
    *,
    color: tuple[int, int, int] = (1, 2, 3),
    is_on: bool = True,
) -> SectionInternalRepresentation:
    return SectionInternalRepresentation(
        section_id, (0, 4), [color] * 5, is_on, name=section_id.upper()
    )


class TestBuildHaRefreshMessages(TestCase):
    """Tests for `build_ha_refresh_messages`."""

    def test_order_offline_discovery_online_state(self) -> None:
        """Messages are ordered offline, discovery, online, state."""
        messages = build_ha_refresh_messages(
            [_section("old")], [_section("a"), _section("b")], 100
        )
        self.assertEqual(
            [
                build_ha_availability_topic("old"),
                build_ha_discovery_topic("a"),
                build_ha_discovery_topic("b"),
                build_ha_availability_topic("a"),
                build_ha_availability_topic("b"),
                build_ha_state_topic("a"),
                build_ha_state_topic("b"),
            ],
            list(messages),
        )
        self.assertEqual("offline", messages[build_ha_availability_topic("old")])
        self.assertEqual("online", messages[build_ha_availability_topic("a")])

    def test_discovery_has_cross_availability(self) -> None:
        """Each discovery declares mode `all` and the global and entity topics."""
        messages = build_ha_refresh_messages([], [_section("a")], 100)
        data = json.loads(messages[build_ha_discovery_topic("a")].to_json())
        self.assertEqual("all", data["availability_mode"])
        self.assertEqual(
            [
                {"topic": "scrpi/status"},
                {"topic": build_ha_availability_topic("a")},
            ],
            data["availability"],
        )
        self.assertNotIn("availability_topic", data)

    def test_no_offline_for_ids_in_both_lists(self) -> None:
        """A kept section is only marked online."""
        messages = build_ha_refresh_messages(
            [_section("a"), _section("old")], [_section("a")], 100
        )
        self.assertEqual("online", messages[build_ha_availability_topic("a")])
        self.assertEqual("offline", messages[build_ha_availability_topic("old")])
        self.assertEqual(
            [
                build_ha_availability_topic("old"),
                build_ha_discovery_topic("a"),
                build_ha_availability_topic("a"),
                build_ha_state_topic("a"),
            ],
            list(messages),
        )

    def test_no_previous_sections(self) -> None:
        """At startup there is no offline message."""
        messages = build_ha_refresh_messages([], [_section("a")], 100)
        self.assertEqual(
            [
                build_ha_discovery_topic("a"),
                build_ha_availability_topic("a"),
                build_ha_state_topic("a"),
            ],
            list(messages),
        )
        discovery = json.loads(messages[build_ha_discovery_topic("a")].to_json())
        self.assertEqual("A", discovery["name"])

    def test_state_has_on_off_color_and_brightness(self) -> None:
        """Each state reflects its section."""
        messages = build_ha_refresh_messages(
            [], [_section("a"), _section("b", color=(0, 255, 0), is_on=False)], 77
        )
        on = json.loads(messages[build_ha_state_topic("a")].to_json())
        off = json.loads(messages[build_ha_state_topic("b")].to_json())
        self.assertEqual("ON", on["state"])
        self.assertEqual(77, on["brightness"])
        self.assertEqual({"r": 1, "g": 2, "b": 3}, on["color"])
        self.assertEqual("OFF", off["state"])
        self.assertEqual({"r": 0, "g": 255, "b": 0}, off["color"])
        self.assertEqual(77, off["brightness"])
