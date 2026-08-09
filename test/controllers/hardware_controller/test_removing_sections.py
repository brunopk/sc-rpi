"""Tests for src/controllers/hardware_controller.py."""

import logging
from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.config.main import load_configurations


class TestRemovingSections(TestCase):
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

    def test_removing_all_sections(self) -> None:
        """Test case test_removing_all_sections."""
        self.controller.new_section("s", 0, 10, (0, 0, 0))
        self.controller.remove_all_sections()
        self.controller.new_section("s", 2, 20, (0, 0, 0))

    def test_removing_specific_sections(self) -> None:
        """Test case test_removing_specific_sections."""
        self.controller.new_section("s_1", 0, 9, (0, 0, 0))
        s2 = self.controller.new_section("s_2", 10, 19, (0, 0, 0))
        s3 = self.controller.new_section("s_3", 20, 29, (0, 0, 0))
        s4 = self.controller.new_section("s_4", 30, 39, (0, 0, 0))
        self.controller.remove_sections([])
        self.assertRaises(ApiError, self.controller.remove_sections, ["asd"])
        self.controller.remove_sections([s2.id, s3.id])
        self.assertRaises(ApiError, self.controller.remove_sections, [s2.id, s4.id])
        self.controller.remove_sections([s4.id])

    def test_setting_color_for_deleted_section(self) -> None:
        """Test case test_setting_color_for_deleted_section."""
        section_id = self.controller.new_section("s_1", 1, 1, (0, 0, 0))
        self.controller.remove_all_sections()
        self.assertRaises(ApiError, self.controller.edit_section, (0, 0, 0), section_id)

