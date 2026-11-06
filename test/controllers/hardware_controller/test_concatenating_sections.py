"""Tests for `_concatenate_sections` in src/controllers/hardware_controller.py."""

from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.controllers.hardware_controller import _concatenate_sections
from sc_rpi.models.section_internal_representation import SectionInternalRepresentation
from sc_rpi.utils.config.main import load_configurations

_OFF = (0, 0, 0)
_RED = (255, 0, 0)
_BLUE = (0, 0, 255)


class TestConcatenatingSections(TestCase):
    """Tests for `_concatenate_sections`."""

    def test_no_sections(self) -> None:
        """No sections give an empty list."""
        self.assertEqual([], _concatenate_sections([], 10))

    def test_gaps_are_filled_with_black(self) -> None:
        """Leds before, between and after sections are (0, 0, 0)."""
        sections = [
            SectionInternalRepresentation("a", (2, 3), [_RED] * 2, is_on=True),
            SectionInternalRepresentation("b", (6, 7), [_BLUE] * 2, is_on=True),
        ]

        colors = _concatenate_sections(sections, 10)

        self.assertEqual(
            [_OFF, _OFF, _RED, _RED, _OFF, _OFF, _BLUE, _BLUE, _OFF, _OFF],
            colors,
        )

    def test_section_that_is_off_is_black(self) -> None:
        """A section that is off has all its leds black."""
        sections = [
            SectionInternalRepresentation("a", (0, 1), [_RED] * 2, is_on=False),
            SectionInternalRepresentation("b", (2, 3), [_BLUE] * 2, is_on=True),
        ]

        colors = _concatenate_sections(sections, 4)

        self.assertEqual([_OFF, _OFF, _BLUE, _BLUE], colors)

    def test_last_section_that_is_off_is_black(self) -> None:
        """The last section also honors `is_on` when there are several sections."""
        sections = [
            SectionInternalRepresentation("a", (0, 1), [_RED] * 2, is_on=True),
            SectionInternalRepresentation("b", (2, 3), [_BLUE] * 2, is_on=False),
        ]

        colors = _concatenate_sections(sections, 4)

        self.assertEqual([_RED, _RED, _OFF, _OFF], colors)

    def test_off_section_in_any_position_is_black(self) -> None:
        """Only the sections that are on keep their color, wherever they are."""
        for is_on in [(False, True, True), (True, False, True), (True, True, False)]:
            with self.subTest(is_on=is_on):
                sections = [
                    SectionInternalRepresentation(
                        str(n),
                        (n * 2, n * 2 + 1),
                        [_RED] * 2,
                        is_on=state,
                    )
                    for n, state in enumerate(is_on)
                ]

                colors = _concatenate_sections(sections, 6)

                expected = []
                for state in is_on:
                    expected += [_RED if state else _OFF] * 2
                self.assertEqual(expected, colors)

    def test_controller_state_is_not_changed(self) -> None:
        """Concatenating given sections does not touch the live sections."""
        controller = HardwareController(load_configurations("config_test.yaml"))
        before = controller.list_sections()
        other = [SectionInternalRepresentation("x", (0, 4), [_RED] * 5, is_on=True)]

        colors = _concatenate_sections(other, 300)

        self.assertEqual(300, len(colors))
        self.assertEqual(before, controller.list_sections())
        self.assertEqual(
            _concatenate_sections(before, 300),
            controller.concatenate_sections(),
        )
