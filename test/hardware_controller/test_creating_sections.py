"""Tests for src/controllers/hardware_controller.py."""

import logging
from configparser import ConfigParser
from random import randint
from unittest import TestCase

from controllers import HardwareController
from errors import ApiError


class TestCreatingSections(TestCase):
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

    def test_wrong_indexes(self) -> None:
        """Test case test_wrong_indexes."""
        self.assertRaises(ApiError, self.controller.new_section, -1, 10, (0, 0, 0))
        self.assertRaises(ApiError, self.controller.new_section, 0, 400, (0, 0, 0))
        self.assertRaises(ApiError, self.controller.new_section, 2, 1, (0, 0, 0))

    def test_overlapping(self) -> None:
        """Test case test_overlapping."""
        self.controller.new_section(1, 100, (0, 0, 0))
        self.assertRaises(ApiError, self.controller.new_section, 50, 300, (0, 0, 0))

    def test_colors_1(self) -> None:
        """Test case test_colors_1."""
        color = (1, 2, 3)
        section_id = self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.edit_section(section_id, color=color)
        self.assertEqual(color, self.controller.concatenate_sections()[0])

    def test_total_length_1(self) -> None:
        """Test case test_total_length_1."""
        self.controller.new_section(0, 100, (0, 0, 0))
        self.assertEqual(
            self.controller.strip_length,
            len(self.controller.concatenate_sections()),
            'It must be the length of the strip'
        )

    def test_colors_2(self) -> None:
        """Test case test_colors_2."""
        s1 = (0, 99)
        s2 = (100, 149)
        s3 = (150, 299)
        color_s1 = (1, 1, 1)
        color_s2 = (2, 2, 2)
        color_s3 = (3, 3, 3)
        self.controller.new_section(s1[0], s1[1], color_s1)
        self.controller.new_section(s2[0], s2[1], color_s2)
        self.controller.new_section(s3[0], s3[1], color_s3)

        colors = self.controller.concatenate_sections()

        s1_color_1 = colors[randint(*s1)]
        s1_color_2 = colors[randint(*s1)]

        s2_color_1 = colors[randint(*s2)]
        s2_color_2 = colors[randint(*s2)]

        s3_color_1 = colors[randint(*s3)]
        s3_color_2 = colors[randint(*s3)]

        self.assertEqual(s1_color_1[0], s1_color_2[0])
        self.assertEqual(s1_color_1[1], s1_color_2[1])
        self.assertEqual(s1_color_1[2], s1_color_2[2])

        self.assertEqual(s2_color_1[0], s2_color_2[0])
        self.assertEqual(s2_color_1[1], s2_color_2[1])
        self.assertEqual(s2_color_1[2], s2_color_2[2])

        self.assertEqual(s3_color_1[0], s3_color_2[0])
        self.assertEqual(s3_color_1[1], s3_color_2[1])
        self.assertEqual(s3_color_1[2], s3_color_2[2])

    def test_total_length_2(self) -> None:
        """Test case test_colors_2."""
        self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.new_section(110, 150, (0, 0, 0))
        self.controller.new_section(151, 299, (0, 0, 0))
        self.assertEqual(
            self.controller.strip_length,
            len(self.controller.concatenate_sections()),
            'It must be the length of the strip'
        )
