from controller import Controller
from configparser import ConfigParser
from rpi_ws218x import Color
from random import randint
import logging
import unittest


class TestCreatingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('../config.ini')
        logging.basicConfig(level=None)
        cls.controller = Controller(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_wrong_indexes(self):
        self.assertRaises(ValueError, self.controller.new_section, -1, 10)
        self.assertRaises(ValueError, self.controller.new_section, 0, 400)
        self.assertRaises(ValueError, self.controller.new_section, 2, 1)

    def test_overlapping(self):
        self.controller.new_section(1, 100)
        self.assertRaises(ValueError, self.controller.new_section, 50, 300)

    def test_colors_in_each_section(self):
        s1 = (0, 99)
        s2 = (100, 149)
        s3 = (150, 299)
        s1_id = self.controller.new_section(*s1)
        s2_id = self.controller.new_section(*s2)
        s3_id = self.controller.new_section(*s3)
        color_s1 = [Color(1, 1, 1)] * (s1[1] - s1[0] + 1)
        color_s2 = [Color(2, 2, 2)] * (s2[1] - s2[0] + 1)
        color_s3 = [Color(3, 3, 3)] * (s3[1] - s3[0] + 1)
        self.controller.set_color_list(s1_id, color_s1)
        self.controller.set_color_list(s2_id, color_s2)
        self.controller.set_color_list(s3_id, color_s3)
        colors = self.controller.concatenate_sections()

        s1_color_1 = colors[randint(*s1)]
        s1_color_2 = colors[randint(*s1)]

        s2_color_1 = colors[randint(*s2)]
        s2_color_2 = colors[randint(*s2)]

        s3_color_1 = colors[randint(*s3)]
        s3_color_2 = colors[randint(*s3)]

        self.assertEqual(s1_color_1.r, s1_color_2.r)
        self.assertEqual(s1_color_1.g, s1_color_2.g)
        self.assertEqual(s1_color_1.b, s1_color_2.b)

        self.assertEqual(s2_color_1.r, s2_color_2.r)
        self.assertEqual(s2_color_1.g, s2_color_2.g)
        self.assertEqual(s2_color_1.b, s2_color_2.b)

        self.assertEqual(s3_color_1.r, s3_color_2.r)
        self.assertEqual(s3_color_1.g, s3_color_2.g)
        self.assertEqual(s3_color_1.b, s3_color_2.b)


class TestRemovingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('../config.ini')
        logging.basicConfig(level=None)
        cls.controller = Controller(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_removing_section(self):
        self.controller.new_section(0, 10)
        self.controller.remove_all_sections()
        self.controller.new_section(2, 20)

    def test_setting_color_for_deleted_section(self):
        color_list = [Color(0, 0, 0)]
        section_id = self.controller.new_section(1, 1)
        self.controller.remove_all_sections()
        self.assertRaises(KeyError, self.controller.set_color_list, section_id, color_list)


class TestSettingColors(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('../config.ini')
        logging.basicConfig(level=None)
        cls.controller = Controller(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_setting_color_with_long_array(self):
        color_list = [Color(0, 0, 0)] * 2
        section_id = self.controller.new_section(1, 1)
        self.assertRaises(ValueError, self.controller.set_color_list, section_id, color_list)


class TestConcatenatingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('../config.ini')
        logging.basicConfig(level=None)
        cls.controller = Controller(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_length_after_concatenating_sections_1(self):
        self.controller.new_section(0, 100)
        self.controller.new_section(110, 150)
        self.controller.new_section(151, 299)
        color_list = self.controller.concatenate_sections()
        self.assertEqual(len(color_list), self.controller.strip_length, 'It must be the length of the strip')

    def test_length_after_concatenating_sections_2(self):
        self.controller.new_section(110, 150)
        self.controller.new_section(0, 100)
        self.controller.new_section(151, 299)
        color_list = self.controller.concatenate_sections()
        self.assertEqual(len(color_list), self.controller.strip_length, 'It must be the length of the strip')


class TestEditingSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser()
        config.read('../config.ini')
        logging.basicConfig(level=None)
        cls.controller = Controller(config=config)

    def setUp(self) -> None:
        self.controller.remove_all_sections()

    def test_editing_section(self):
        section_id = self.controller.new_section(0, 100)
        self.controller.edit_section(section_id, 20, 100)


if __name__ == '__main__':
    unittest.main()
