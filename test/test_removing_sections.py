"""Tests for src/controllers/hardware_controller.py."""

import logging
from configparser import ConfigParser
from unittest import TestCase

from controllers import HardwareController


class TestRemovingSections(TestCase):
    """Tests for src/controllers/hardware_controller.py."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        config = ConfigParser()
        config.read("./config.ini")
        logging.basicConfig(level=None)
        cls.controller = HardwareController(config=config)

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        self.controller.remove_all_sections()

    def test_removing_all_sections(self) -> None:
        """Test case test_removing_all_sections."""
        self.controller.new_section(0, 10, (0, 0, 0))
        self.controller.remove_all_sections()
        self.controller.new_section(2, 20, (0, 0, 0))

    def test_removing_specific_sections(self) -> None:
        """Test case test_removing_specific_sections."""
        self.controller.new_section(0, 9, (0, 0, 0))
        s2_id = self.controller.new_section(10, 19, (0, 0, 0))
        s3_id = self.controller.new_section(20, 29, (0, 0, 0))
        s4_id = self.controller.new_section(30, 39, (0, 0, 0))
        self.controller.remove_sections([])
        self.assertRaises(KeyError, self.controller.remove_sections, [''])
        self.controller.remove_sections([s2_id, s3_id])
        self.assertRaises(KeyError, self.controller.remove_sections, [s2_id, s4_id])
        self.controller.remove_sections([s4_id])

    def test_setting_color_for_deleted_section(self) -> None:
        """Test case test_setting_color_for_deleted_section."""
        section_id = self.controller.new_section(1, 1, (0, 0, 0))
        self.controller.remove_all_sections()
        self.assertRaises(KeyError, self.controller.edit_section, (0, 0, 0), section_id)

