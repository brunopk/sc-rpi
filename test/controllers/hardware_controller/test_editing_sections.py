"""Tests for src/controllers/hardware_controller.py."""

import logging
from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config.main import load_configurations


class TestEditingSections(TestCase):
    """Tests for src/controllers/hardware_controller.py."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        config = load_configurations()
        logging.basicConfig(level=None)
        cls.controller = HardwareController(config=config)

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        self.controller.remove_all_sections()

    def test_length(self) -> None:
        """Test case test_length."""
        section = self.controller.new_section("s", 0, 100, (0, 0, 0))
        self.controller.edit_section(section.id, 20, 100)
        self.assertEqual(
            self.controller._strip_length,
            len(self.controller.concatenate_sections()),
            "It must be the length of the strip",
        )

    def test_editing_sections(self) -> None:
        """Test case test_colors."""
        new_color = (1, 2, 3)
        section = self.controller.new_section("s", 0, 100, (0, 0, 0))
        self.controller.edit_section(section.id, 20, 100)
        self.controller.edit_section(section.id, color=new_color)
        self.controller.render()

        # Verify that other sections remains unmodified
        self.assertEqual((0, 0, 0), self.controller.concatenate_sections()[0])

        # Verify only the corresponding section is modified
        self.assertEqual(new_color, self.controller.concatenate_sections()[21])
