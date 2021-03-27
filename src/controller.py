import logging
from typing import List
from rpi_ws281x import PixelStrip, Color
from configparser import ConfigParser
from uuid import uuid1
from utils import bool


class Section:

    def __init__(self, indexes: tuple, color_list: List[tuple]):
        self.indexes = indexes
        self.color_list = color_list

    def get_indexes(self) -> tuple:
        return self.indexes

    def get_color_list(self) -> List[tuple]:
        return self.color_list


class SectionManager:

    def _insert_section(self, section_id: str, index: int, start: int, end: int, color_list):
        self.ids.insert(index, section_id)
        self.color_list.insert(index, color_list)
        self.color_list_by_id[section_id] = color_list
        self.limits_by_id[section_id] = (start, end)
        self.limits.insert(index, (start, end))

    def _remove_section(self, section_id: str):
        """
        :raise KeyError: if section don't exist
        """
        t = self.limits_by_id[section_id]
        i = self.limits.index(t)
        del self.ids[i]
        del self.color_list[i]
        del self.limits_by_id[section_id]
        del self.limits[i]

    def _get_index(self, start: int, end: int):
        """
        Get index position in the self.ids (same for self.color_list and self.limits)
        array of the section defined by [start, end]

        :raises ValueError: if limits are not defined correctly (section overlapping, etc)
        """

        index = None

        if end < start or start < 0 or end > self.strip_length:
            raise ValueError('section not defined correctly')
        for i, v in enumerate(self.limits):
            if v[0] < start < v[1] or v[0] < end < v[1]:
                raise ValueError('overlapping error')
            if i < len(self.limits) - 1:
                if self.limits[i][0] < start and end < self.limits[i + 1][0]:
                    index = i + 1
                    break
            elif index is None:
                if start > self.limits[i][1]:
                    index = i + 1
                else:
                    index = i

        return 0 if index is None else index

    def __init__(self, config: ConfigParser):
        self.strip_length = int(config['PIXEL_STRIP'].get('n'))
        self.config = config
        self.ids = []
        self.color_list = []
        self.color_list_by_id = {}
        self.limits_by_id = {}
        self.limits = []

    def edit_section(self,
                     section_id: str,
                     new_start: int = None,
                     new_end: int = None,
                     new_color_list: List[tuple] = None):
        """
        Edit section

        :raises KeyError: if section not exist
        :raises ValueError: if limits are defined correctly (section overlapping, etc)
        """

        try:
            index = self.ids.index(section_id)
        except ValueError:
            raise KeyError()

        start, end = self.limits_by_id[section_id]
        new_start = new_start if new_start is not None else self.limits_by_id[section_id][0]
        new_end = new_end if new_end is not None else self.limits_by_id[section_id][1]
        if new_color_list is not None:
            if len(new_color_list) != new_end - new_start + 1:
                raise ValueError('length of the color list does not match the new size of the section')
        else:
            color_list = self.color_list_by_id[section_id]
            new_color_list = [color_list[0]] * (new_end - new_start + 1)

        self.limits.remove((start, end))
        self.ids.remove(section_id)
        del self.color_list[index]

        index = self._get_index(new_start, new_end)
        self._insert_section(section_id, index, new_start, new_end, new_color_list)

    def new_section(self, start: int, end: int) -> str:
        """
        Creates new section

        :raises ValueError: if limits are defined correctly (also in case of section overlapping)
        """
        section_id = str(uuid1())
        color_list = [(0, 0, 0)] * (end - start + 1)
        index = self._get_index(start, end)
        self._insert_section(section_id, index, start, end, color_list)
        return section_id

    def set_color(self, section_id: str, color_list: List[tuple]):
        """
        Sets the color for each led in the specified section

        :param section_id: identifier of the section that will be updated
        :param color_list: colors for each led in the section
        :raises KeyError: if section is not defined
        :raises ValueError: if color_list is longer than the size of the section
        """
        limits = self.limits_by_id.get(section_id)
        if limits is None:
            raise KeyError(f'section {section_id} is not defined')
        if len(color_list) != (limits[1] - limits[0] + 1):
            raise ValueError(f'color array length does not match section {section_id} length')
        self.color_list[self.ids.index(section_id)] = color_list
        self.color_list_by_id[section_id] = color_list

    def get_section(self, section_id: str) -> Section:
        """
        Finds and returns a section

        :param section_id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return Section(self.limits_by_id[section_id], self.color_list_by_id[section_id])

    def get_all_sections(self) -> List[Section]:
        """
        Returns all sections ordered by (start, end) indexes of the sections
        """
        return [Section(self.limits[i], self.color_list[i]) for i in range(len(self.limits))]

    def remove_all_sections(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self.ids = []
        self.color_list = []
        self.color_list_by_id = {}
        self.limits_by_id = {}
        self.limits = []

    def remove_sections(self, sections: List[str]):
        """
        Removes sections by id
        :param sections: list of section ids to be removed
        :raise KeyError: if some section don't exist
        """
        # test if all sections are defined
        invalid_section_id = None
        for section_id in sections:
            if section_id not in self.limits_by_id:
                invalid_section_id = section_id
                break
        # remove sections (if all sections are defined)
        if invalid_section_id is None:
            for section_id in sections:
                self._remove_section(section_id)
        else:
            raise KeyError(f'section {section_id} is not defined')


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
        self.logger = logging.getLogger(str(self.__class__))
        self.section_manager = SectionManager(config)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()

    def new_section(self, start: int, end: int) -> str:
        """
        Defines a new section on the strip

        :param start: start position of the section
        :param end: end position of the section
        :return: uuid of the section
        :raises ValueError: if limits are defined correctly (also in case of section overlapping)
        """
        return self.section_manager.new_section(start, end)

    def edit_section(self, section_id: str, start: int = None, end: int = None, color_list: List[tuple] = None):
        """
        Changes the start position and/or end position and/or each color of each led of the specified section

        :param section_id: id of the section that will be edited
        :param start: new start position for the section
        :param end: new end position for the section
        :param color_list: color for each led in the section
        :raises KeyError: if section with section_id is not defined
        :raises ValueError: if limits are defined correctly (also in case of section overlapping)
        """
        return self.section_manager.edit_section(section_id, start, end, color_list)

    def get_section(self, section_id: str) -> Section:
        """
        Finds and returns a section

        :param section_id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return self.section_manager.get_section(section_id)

    def get_strip_length(self) -> int:
        return self.strip_length

    def set_color(self, color: tuple, section_id: str = None):
        """
        Sets the same color for all LEDs in the strip or for LEDs in a specific section

        :param color: the new color
        :param section_id: if it is defined, sets the color ONLY for LEDs in that section
        :raises KeyError: if section with section_id is not defined
        """
        if section_id is None:
            self.current_color = color
        else:
            section = self.section_manager.get_section(section_id)
            new_color_list = [color] * (section.get_indexes()[1] - section.get_indexes()[0] + 1)
            self.section_manager.set_color(section_id, new_color_list)

    def remove_sections(self, sections: List[str]):
        """
        Removes sections by id
        :param sections: list of section ids to be removed
        :raise KeyError: if some section don't exist
        """
        self.section_manager.remove_sections(sections)

    def remove_all_sections(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self.section_manager.remove_all_sections()

    def concatenate_sections(self) -> List[tuple]:
        """
        Concatenates all sections in one list.
        Spaces between section will be filled with Color(0, 0, 0)

        :return: a list with the length of the strip or void list if no sections are defined
        """
        colors = []
        sections = self.section_manager.get_all_sections()
        cant_sections = len(sections)
        if cant_sections > 0:
            colors += [(0, 0, 0)] * sections[0].get_indexes()[0]
            for i, section in enumerate(sections[0:-1]):
                colors += section.get_color_list()
                colors += [(0, 0, 0)] * (sections[i + 1].get_indexes()[0] - section.get_indexes()[1] - 1)
            if cant_sections > 1:
                colors += [(0, 0, 0)] * (sections[-1].get_indexes()[0] - sections[-2].get_indexes()[1] - 1)
                colors += sections[-1].get_color_list()
                colors += [(0, 0, 0)] * (self.strip_length - sections[-1].get_indexes()[1] - 1)
        return colors

    def render_strip(self):
        """
        Renders the actual configuration on the strip (hardware)
        """
        colors = self. concatenate_sections()
        # TODO cuando uso edit section no me entra aca
        if len(colors) > 0:
            for i, c in enumerate(colors):
                self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))
        else:
            for i in range(self.strip_length):
                self.strip.setPixelColor(i, self.current_color)
        self.strip.show()

    def exec_cmd(self, cmd) -> dict:
        """
        Executes the current command (see set_command) on the current section (see set_section).
        If no section was set, executes the command on the entire strip.

        :return: result of the execution
        """
        cmd.set_controller(self)
        return cmd.exec()
