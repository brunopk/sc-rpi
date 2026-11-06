"""Tests for `get_current_config` in the hardware controller."""

from __future__ import annotations

from dataclasses import replace
from unittest import TestCase

from sc_rpi.config.strip import Section
from sc_rpi.controllers import HardwareController
from sc_rpi.models import Color
from sc_rpi.utils.config.main import load_configurations

_FIRST_ID = "ws2812b_strip_section_1"


class TestGettingCurrentConfig(TestCase):
    """Tests for `get_current_config`."""

    def setUp(self) -> None:
        """Create a controller from the test config."""
        self.config = load_configurations("config_test.yaml")
        self.controller = HardwareController(self.config)

    def _first_section(self) -> Section:
        current = self.controller.get_current_config()
        return next(s for s in current.strip.sections if s.id == _FIRST_ID)

    def test_matches_boot_config_at_start(self) -> None:
        """Before any change the current config equals the boot config."""
        self.assertEqual(self.config, self.controller.get_current_config())

    def test_includes_edit_section(self) -> None:
        """An edited section shows up with its new range and color."""
        self.controller.edit_section(_FIRST_ID, start=10, end=20, color=(1, 2, 3))

        section = self._first_section()

        self.assertEqual((10, 20), (section.start, section.end))
        self.assertEqual(Color(1, 2, 3), section.color)

    def test_includes_turn_section_on_and_off(self) -> None:
        """Turning a section on and off shows up in `is_on`."""
        self.controller.turn_section_on(_FIRST_ID, (0, 255, 0))
        self.assertTrue(self._first_section().is_on)

        self.controller.turn_section_off(_FIRST_ID)

        section = self._first_section()
        self.assertFalse(section.is_on)
        self.assertEqual(Color(0, 255, 0), section.color)

    def test_includes_applied_config(self) -> None:
        """An applied config replaces the sections and the description."""
        new_section = Section(
            color=Color(9, 8, 7),
            end=50,
            id="party_section_1",
            is_on=False,
            name="Party",
            start=40,
        )
        loaded = replace(
            self.config,
            strip=replace(self.config.strip, sections=[new_section]),
            description="Friday lights",
        )
        prepared = self.controller.prepare_config(loaded)
        self.controller.apply_prepared(prepared, loaded.description)

        current = self.controller.get_current_config()

        self.assertEqual([new_section], current.strip.sections)
        self.assertEqual("Friday lights", current.description)

    def test_boot_config_is_not_modified(self) -> None:
        """Reading the current config never changes the boot `Config`."""
        before = load_configurations("config_test.yaml")
        self.controller.edit_section(_FIRST_ID, color=(1, 2, 3))

        self.controller.get_current_config()

        self.assertEqual(before, self.config)
