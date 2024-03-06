import logging
import unittest
from hardware_controller import HardwareController
from configparser import ConfigParser
from random import randint


class TestCreatingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        logging.basicConfig(level=None)
        cls.controller = HardwareController(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_wrong_indexes(self):
        self.assertRaises(ValueError, self.controller.new_section, -1, 10, (0, 0, 0))
        self.assertRaises(ValueError, self.controller.new_section, 0, 400, (0, 0, 0))
        self.assertRaises(ValueError, self.controller.new_section, 2, 1, (0, 0, 0))

    def test_overlapping(self):
        self.controller.new_section(1, 100, (0, 0, 0))
        self.assertRaises(Overlapping, self.controller.new_section, 50, 300, (0, 0, 0))

    def test_colors_1(self):
        color = (1, 2, 3)
        section_id = self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.edit_section(section_id, color=color)
        self.assertEqual(color, self.controller.concatenate_sections()[0])

    def test_total_length_1(self):
        self.controller.new_section(0, 100, (0, 0, 0))
        self.assertEqual(
            self.controller.strip_length,
            len(self.controller.concatenate_sections()),
            'It must be the length of the strip'
        )

    def test_colors_2(self):
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

    def test_total_length_2(self):
        self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.new_section(110, 150, (0, 0, 0))
        self.controller.new_section(151, 299, (0, 0, 0))
        self.assertEqual(
            self.controller.strip_length,
            len(self.controller.concatenate_sections()),
            'It must be the length of the strip'
        )


class TestRemovingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        logging.basicConfig(level=None)
        cls.controller = HardwareController(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_removing_all_sections(self):
        self.controller.new_section(0, 10, (0, 0, 0))
        self.controller.remove_all_sections()
        self.controller.new_section(2, 20, (0, 0, 0))

    def test_removing_specific_sections(self):
        self.controller.new_section(0, 9, (0, 0, 0))
        s2_id = self.controller.new_section(10, 19, (0, 0, 0))
        s3_id = self.controller.new_section(20, 29, (0, 0, 0))
        s4_id = self.controller.new_section(30, 39, (0, 0, 0))
        self.controller.remove_sections([])
        self.assertRaises(KeyError, self.controller.remove_sections, [''])
        self.controller.remove_sections([s2_id, s3_id])
        self.assertRaises(KeyError, self.controller.remove_sections, [s2_id, s4_id])
        self.controller.remove_sections([s4_id])

    def test_setting_color_for_deleted_section(self):
        section_id = self.controller.new_section(1, 1, (0, 0, 0))
        self.controller.remove_all_sections()
        self.assertRaises(KeyError, self.controller.set_color, (0, 0, 0), section_id)


class TestEditingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('./config.ini')
        logging.basicConfig(level=None)
        cls.controller = HardwareController(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_length(self):
        section_id = self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.edit_section(section_id, 20, 100)
        self.assertEqual(
            self.controller.strip_length,
            len(self.controller.concatenate_sections()),
            'It must be the length of the strip'
        )

    def test_colors(self):
        color = (1, 2, 3)
        section_id = self.controller.new_section(0, 100, (0, 0, 0))
        self.controller.edit_section(section_id, 20, 100)
        self.controller.set_color(color, section_id)
        self.controller.render()
        self.assertEqual((0, 0, 0), self.controller.concatenate_sections()[0])
        self.assertEqual(color, self.controller.concatenate_sections()[21])


if __name__ == '__main__':
    unittest.main()
