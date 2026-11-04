"""Tests for `SectionsController`."""

from __future__ import annotations

from dataclasses import replace
from unittest import TestCase

from sc_rpi.config import Config
from sc_rpi.config.strip import Section
from sc_rpi.controllers.sections_controller import SectionsController
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color
from sc_rpi.utils.config import load_configurations


def config_with_sections(sections: list[Section]) -> Config:
    """Build a config (from the test config) with the given sections."""
    config = load_configurations("config_test.yaml")
    return replace(config, strip=replace(config.strip, sections=sections))


def section(
    section_id: str,
    start: int,
    end: int,
    *,
    is_on: bool = True,
    color: Color | None = None,
    name: str | None = None,
) -> Section:
    """Build a config section."""
    return Section(
        color=color or Color(255, 255, 255),
        end=end,
        id=section_id,
        is_on=is_on,
        name=name or section_id,
        start=start,
    )


class TestSectionsController(TestCase):
    """Tests for `SectionsController`."""

    def empty_controller(self) -> SectionsController:
        """Create a controller without sections."""
        return SectionsController(config_with_sections([]))

    def test_turn_off_and_on_keeps_state_consistent(self) -> None:
        """Ordered lists and by-id lookups agree after turning sections off/on."""
        controller = SectionsController(
            config_with_sections(
                [section("a", 0, 9), section("b", 10, 19), section("c", 20, 29)]
            )
        )

        controller.turn_section_off("b")
        self._assert_consistent(controller)
        self.assertEqual(
            [True, False, True], [s.is_on for s in controller.list_sections()]
        )

        controller.turn_section_on("b", (1, 2, 3))
        self._assert_consistent(controller)
        self.assertEqual(
            [True, True, True], [s.is_on for s in controller.list_sections()]
        )
        self.assertEqual((1, 2, 3), controller.get_section("b").color_list[0])
        self.assertEqual((255, 255, 255), controller.get_section("a").color_list[0])

    def test_turn_off_first_section_does_not_change_others(self) -> None:
        """Turning off a section leaves the other ones as they were."""
        controller = SectionsController(
            config_with_sections([section("a", 0, 9), section("b", 10, 19)])
        )
        controller.turn_section_off("a")
        self.assertEqual(
            [False, True], [s.is_on for s in controller.list_sections()]
        )
        self.assertEqual(2, len(controller.list_sections()))
        self._assert_consistent(controller)

    def test_edit_section_keeps_is_on_in_ordered_list(self) -> None:
        """Editing an off section keeps it off in `list_sections`."""
        controller = SectionsController(
            config_with_sections([section("a", 0, 9, is_on=False)])
        )
        controller.edit_section("a", end=20)
        self.assertFalse(controller.list_sections()[0].is_on)
        self._assert_consistent(controller)

    def test_overlap_variants_are_rejected(self) -> None:
        """Shared boundary, identical and enclosing ranges overlap."""
        for start, end in [(20, 30), (5, 10), (10, 20), (5, 25), (12, 15), (15, 25)]:
            with self.subTest(start=start, end=end):
                controller = self.empty_controller()
                controller.new_section("s1", 10, 20, is_on=True)
                with self.assertRaises(ApiError) as ctx:
                    controller.new_section("s2", start, end, is_on=True)
                self.assertEqual(ErrorCode.SECTION_OVERLAPPING, ctx.exception.code)
                self.assertEqual(1, len(controller.list_sections()))

    def test_adjacent_sections_are_accepted(self) -> None:
        """Adjacent non-overlapping ranges are accepted and ordered by start."""
        controller = self.empty_controller()
        controller.new_section("s2", 21, 30, is_on=True)
        controller.new_section("s1", 10, 20, is_on=True)
        controller.new_section("s0", 0, 9, is_on=True)
        self.assertEqual(
            ["s0", "s1", "s2"], [s.id for s in controller.list_sections()]
        )
        self._assert_consistent(controller)

    def test_edit_section_overlap_is_rejected(self) -> None:
        """Editing a section so that it touches another one is rejected."""
        controller = SectionsController(
            config_with_sections([section("a", 0, 9), section("b", 10, 19)])
        )
        with self.assertRaises(ApiError) as ctx:
            controller.edit_section("a", end=10)
        self.assertEqual(ErrorCode.SECTION_OVERLAPPING, ctx.exception.code)

    def test_names_come_from_config(self) -> None:
        """Names are stored and returned by `get_section` and `list_sections`."""
        controller = SectionsController(
            config_with_sections(
                [section("a", 0, 9, name="Desk"), section("b", 10, 19, name="Shelf")]
            )
        )
        self.assertEqual("Desk", controller.get_section("a").name)
        self.assertEqual(
            ["Desk", "Shelf"], [s.name for s in controller.list_sections()]
        )
        controller.edit_section("a", end=5)
        self.assertEqual("Desk", controller.get_section("a").name)

    def test_color_and_is_on_come_from_config(self) -> None:
        """Configured color and on/off state are applied."""
        controller = SectionsController(
            config_with_sections(
                [
                    section("off", 0, 9, is_on=False),
                    section("green", 10, 19, color=Color(0, 255, 0)),
                ]
            )
        )
        off = controller.get_section("off")
        green = controller.get_section("green")
        self.assertFalse(off.is_on)
        self.assertEqual((255, 255, 255), off.color_list[0])
        self.assertTrue(green.is_on)
        self.assertEqual((0, 255, 0), green.color_list[0])
        self._assert_consistent(controller)

    def _assert_consistent(self, controller: SectionsController) -> None:
        for listed in controller.list_sections():
            self.assertEqual(listed, controller.get_section(listed.id))
