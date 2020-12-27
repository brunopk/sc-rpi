import logging
from typing import List
from rpi_ws218x import PixelStrip, Color
from configparser import ConfigParser
from uuid import uuid1


class Section:

    def __init__(self, indexes: tuple, array: List[Color], ):
        self.indexes = indexes
        self.array = array

    def get_indexes(self) -> tuple:
        return self.indexes

    def get_array(self) -> List[Color]:
        return self.array


class SectionManager:

    def __init__(self, config: ConfigParser):
        self.config = config
        self.indexes = []
        self.ids = []
        self.arrays = []
        self.indexes_by_id = {}
        self.arrays_by_id = {}
        self.strip_length = int(config['PIXEL_STRIP'].get('n'))

    def reset(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self.indexes = []
        self.ids = []
        self.arrays = []
        self.indexes_by_id = {}
        self.arrays_by_id = {}

    def new_section(self, start: int, end: int) -> str:
        position = len(self.indexes)
        if end < start or start < 0 or end > self.strip_length:
            raise ValueError('section is not defined correctly')
        for i, v in enumerate(self.indexes):
            if v[0] < start < v[1] or v[0] < end < v[1]:
                raise ValueError('the new section overlaps another section')
            if i < len(self.indexes) - 1:
                if self.indexes[i][0] < start and end < self.indexes[i + 1][0]:
                    position = i + 1
                    break
        s_id = str(uuid1())
        array = [Color(0, 0, 0)] * (end - start + 1)
        self.indexes.insert(position, (start, end))
        self.ids.insert(position, s_id)
        self.arrays.insert(position, array)
        self.indexes_by_id[s_id] = (start, end)
        self.arrays_by_id[s_id] = array
        return s_id

    def update_section(self, s_id: str, array: List[Color]):
        """
        Sets the color for each led in the specified section

        :param s_id: identifier of the section that will be updated
        :param array: colors for each led in the section
        :raises KeyError: if section is not defined
        :raises ValueError: if len(array) is more than previously specified length of the section
        """
        indexes = self.indexes_by_id.get(s_id)
        if indexes is None:
            raise KeyError(f'section {s_id} is not defined')
        if len(array) != (indexes[1] - indexes[0] + 1):
            raise ValueError(f'color array length does not match section {s_id} length')
        self.arrays[self.ids.index(s_id)] = array
        self.arrays_by_id[s_id] = array

    def get_section_by_id(self, s_id: str) -> List[Color]:
        """
        Returns the color for each led in the specified section

        :param s_id: identifier of the section
        :raises KeyError: if the section is not defined
        """
        return self.arrays_by_id[s_id]

    def get_all_sections(self) -> List[Section]:
        """
        Returns all sections ordered by (start, end) indexes of the sections
        """
        return [Section(self.indexes[i], self.arrays[i]) for i in range(len(self.ids))]


class Controller:
    """
    Provides an interface to control the strip executing commands on specific sections
    (portions of the strip defined by the starting and ending position).
    """

    def __init__(self, config: ConfigParser):

        n = int(config['PIXEL_STRIP'].get('n'))
        pin = int(config['PIXEL_STRIP'].get('pin'))
        freq_hz = int(config['PIXEL_STRIP'].get('freq_hz'))
        dma = int(config['PIXEL_STRIP'].get('dma'))
        invert = bool(config['PIXEL_STRIP'].get('invert'))
        brightness = int(config['PIXEL_STRIP'].get('brightness'))
        channel = int(config['PIXEL_STRIP'].get('channel'))

        if n is None:
            raise Exception('Cannot initialize controller, n was not set in config.ini')
        if pin is None:
            raise Exception('Cannot initialize controller, pin was not set in config.ini')
        if freq_hz is None:
            raise Exception('Cannot initialize controller, freq_hz was not set in config.ini')
        if dma is None:
            raise Exception('Cannot initialize controller, dma was not set in config.ini')
        if invert is None:
            raise Exception('Cannot initialize controller, invert was not set in config.ini')
        if brightness is None:
            raise Exception('Cannot initialize controller, brightness was not set in config.ini')
        if channel is None:
            raise Exception('Cannot initialize controller, channel was not set in config.ini')

        self.strip_length = n
        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(n, pin, freq_hz, dma, invert, brightness, channel)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()
        self.current_color = Color(0, 0, 0)
        self.logger = logging.getLogger(str(self.__class__))
        self.section_manager = SectionManager(config)

    def new_section(self, start: int, end: int) -> str:
        """
        Defines a new section on the strip

        :param start: start position of the section
        :param end: end position of the section
        :return: uuid of the section
        :raise ValueError: if section is not defined correctly
        """
        return self.section_manager.new_section(start, end)

    def get_section_by_id(self, s_id: str) -> List[Color]:
        """
        Returns the color for each led in the specified section

        :param s_id: identifier of the section
        :raises KeyError: if the section is not defined
        """
        return self.section_manager.get_section_by_id(s_id)

    def get_strip_length(self) -> int:
        return self.strip_length

    def remove_all_sections(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self.section_manager.reset()

    def update_section(self, s_id: str, array: List[Color]):
        """
        Sets the color for each led in the specified section

        :param s_id: identifier of the section that will be updated
        :param array: colors for each led in the section
        :raises KeyError: if section is not defined
        :raises ValueError: if len(array) is more than previously specified len of the section
        """
        self.section_manager.update_section(s_id, array)

    def concatenate_sections(self) -> List[Color]:
        """
        Concatenates all sections in one list.
        Spaces between section will be filled with Color(0, 0, 0)

        :return: a list with the length of the strip or void list if no sections are defined
        """
        colors = []
        sections = self.section_manager.get_all_sections()
        cant_sections = len(sections)
        if cant_sections > 0:
            colors += [Color(0, 0, 0)] * sections[0].get_indexes()[0]
            for i, section in enumerate(sections[0:-1]):
                colors += section.get_array()
                colors += [self.current_color] * (sections[i + 1].get_indexes()[0] - section.get_indexes()[1] - 1)
            if cant_sections > 1:
                colors += [self.current_color] * (sections[-1].get_indexes()[0] - sections[-2].get_indexes()[1] - 1)
                colors += sections[-1].get_array()
                colors += [self.current_color] * (self.strip_length - sections[-1].get_indexes()[1] - 1)
        return colors

    def render_strip(self):
        """
        Renders the actual configuration on the strip (hardware)
        """
        colors = self. concatenate_sections()
        if len(colors) > 0:
            for i, c in enumerate(colors):
                self.strip.setPixelColor(i, c)
        else:
            for i in range(self.strip_length):
                self.strip.setPixelColor(i, self.current_color)
        self.strip.show()

    def set_color(self, color: Color):
        """
        Sets the same color for each led in the strip
        """
        self.current_color = color

    def run_command(self, cmd) -> dict:
        """
        Executes the current command (see set_command) on the current section (see set_section).
        If no section was set, executes the command on the entire strip.

        :return: result of the execution
        """
        cmd.set_controller(self)
        return cmd.exec()
