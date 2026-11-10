"""Tests for `prepare_config` and `apply_prepared` in the hardware controller."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING
from unittest import TestCase
from unittest.mock import patch

from sc_rpi.config.strip import Section
from sc_rpi.controllers import HardwareController
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color
from sc_rpi.utils.config.main import load_configurations

if TYPE_CHECKING:
    from sc_rpi.config import Config


def _section(section_id: str, start: int, end: int, *, is_on: bool = True) -> Section:
    return Section(
        color=Color(0, 255, 0),
        end=end,
        id=section_id,
        is_on=is_on,
        name=section_id.upper(),
        start=start,
    )


class TestApplyingConfig(TestCase):
    """Tests for `prepare_config` and `apply_prepared`."""

    def setUp(self) -> None:
        """Create a controller from the test config."""
        self.config = load_configurations("config_test.yaml")
        self.controller = HardwareController(self.config)

    def _loaded(self, sections: list[Section], description: str = "new") -> Config:
        strip = replace(self.config.strip, sections=sections)
        return replace(self.config, strip=strip, description=description)

    def test_active_configuration_is_default_at_startup(self) -> None:
        """A new controller (a restart) reports `default` as active."""
        self.assertEqual("default", self.controller.get_active_configuration())

    def test_apply_sets_active_configuration(self) -> None:
        """`apply_prepared` makes the given name the active configuration."""
        loaded = self._loaded([_section("p1", 10, 19)])
        prepared = self.controller.prepare_config(loaded)

        self.controller.apply_prepared(prepared, loaded.description, "party")

        self.assertEqual("party", self.controller.get_active_configuration())

    def test_prepare_leaves_controller_unchanged(self) -> None:
        """Preparing a config builds sections but changes no state."""
        before = self.controller.list_sections()
        loaded = self._loaded([_section("p1", 10, 19), _section("p2", 30, 39)])

        prepared = self.controller.prepare_config(loaded)

        self.assertEqual(["p1", "p2"], [s.id for s in prepared])
        self.assertEqual(before, self.controller.list_sections())
        self.assertEqual(self.config.description, self.controller._description)  # noqa: SLF001

    def test_apply_replaces_sections_and_description(self) -> None:
        """After `apply_prepared` the prepared sections and description are live."""
        loaded = self._loaded([_section("p1", 10, 19, is_on=False)], "Friday lights")
        prepared = self.controller.prepare_config(loaded)

        self.controller.apply_prepared(prepared, loaded.description, "party")

        sections = self.controller.list_sections()
        self.assertEqual(["p1"], [s.id for s in sections])
        self.assertEqual("P1", sections[0].name)
        self.assertEqual((10, 19), sections[0].limits)
        self.assertFalse(sections[0].is_on)
        self.assertEqual("Friday lights", self.controller._description)  # noqa: SLF001
        self.assertEqual("p1", self.controller.get_section("p1").id)

    def test_overlapping_config_is_invalid(self) -> None:
        """Overlapping sections raise INVALID_CONFIG and change nothing."""
        before = self.controller.list_sections()
        loaded = self._loaded([_section("a", 10, 20), _section("b", 20, 30)])

        with self.assertRaises(ApiError) as ctx:
            self.controller.prepare_config(loaded)

        self.assertEqual(ErrorCode.INVALID_CONFIG, ctx.exception.code)
        self.assertEqual(before, self.controller.list_sections())

    def test_section_beyond_strip_length_is_invalid(self) -> None:
        """A section beyond the running strip length raises INVALID_CONFIG."""
        before = self.controller.list_sections()
        # The loaded config says its strip is longer, but the running one is used.
        loaded = self._loaded([_section("a", 290, 310)])
        loaded = replace(loaded, strip=replace(loaded.strip, strip_length=1000))

        with self.assertRaises(ApiError) as ctx:
            self.controller.prepare_config(loaded)

        self.assertEqual(ErrorCode.INVALID_CONFIG, ctx.exception.code)
        self.assertEqual(before, self.controller.list_sections())

    def test_failing_render_leaves_state_unchanged(self) -> None:
        """If rendering raises, sections and description are not replaced."""
        before = self.controller.list_sections()
        loaded = self._loaded([_section("p1", 10, 19)], "new")
        prepared = self.controller.prepare_config(loaded)

        with (
            patch.object(self.controller._strip, "show", side_effect=RuntimeError),  # noqa: SLF001
            self.assertRaises(RuntimeError),
        ):
            self.controller.apply_prepared(prepared, loaded.description, "party")

        self.assertEqual(before, self.controller.list_sections())
        self.assertEqual(self.config.description, self.controller._description)  # noqa: SLF001
        self.assertEqual("default", self.controller.get_active_configuration())
