import logging
from typing import List, Tuple
from webcolors import rgb_to_hex
from rpi_ws281x import PixelStrip, Color
from configparser import ConfigParser
from error import Overlapping, AlreadyOn
from uuid import uuid1
from utils import bool


class Section:

    # noinspection PyShadowingBuiltins
    def __init__(self, id: str, is_on: bool, limits: tuple, color_list: List[tuple]):
        self.id = id
        self.indexes = limits
        self.color_list = color_list
        self.is_on = is_on

    def get_id(self) -> str:
        return self.id

    def get_limits(self) -> tuple:
        return self.indexes

    def get_color_list(self) -> List[tuple]:
        return self.color_list

    def is_on(self) -> bool:
        return self.is_on


class SectionManager:

    # noinspection PyShadowingBuiltins
    def _insert_section(self, id: str, start: int, end: int, color_list):
        """
        :raise ValueError: if start > end
        :raise Overlapping: if the new section overlaps another section
        """
        index = None
        if end < start or start < 0 or end > self.strip_length:
            raise ValueError('section not defined correctly')
        for i, v in enumerate(self.limits):
            if v[0] < start < v[1] or v[0] < end < v[1]:
                raise Overlapping()
            if i < len(self.limits) - 1:
                if self.limits[i][0] < start and end < self.limits[i + 1][0]:
                    index = i + 1
                    break
            elif index is None:
                if start > self.limits[i][1]:
                    index = i + 1
                else:
                    index = i
        index = 0 if index is None else index

        self.is_on.insert(index, True)
        self.ids.insert(index, id)
        self.color_list.insert(index, color_list)
        self.limits.insert(index, (start, end))
        self.color_list_by_id[id] = color_list
        self.limits_by_id[id] = (start, end)
        self.is_on_by_id[id] = True

    def _remove_section(self, id: str):
        """
        :raise KeyError: if section don't exist
        """
        t = self.limits_by_id[id]
        i = self.limits.index(t)
        del self.ids[i]
        del self.color_list[i]
        del self.limits[i]
        del self.is_on[i]
        del self.color_list_by_id[id]
        del self.limits_by_id[id]
        del self.is_on_by_id[id]

    def __init__(self, config: ConfigParser):
        self.strip_length = int(config['PIXEL_STRIP'].get('n'))
        self.config = config
        self.ids = []
        self.color_list = []
        self.limits = []
        self.is_on = []
        self.color_list_by_id = {}
        self.limits_by_id = {}
        self.is_on_by_id = {}

    # noinspection PyShadowingBuiltins
    def edit_section(self, id: str, new_start: int = None, new_end: int = None, new_color_list: List[tuple] = None):
        """
        Edits a section

        :raise KeyError: if section not exist
        :raise ValueError: if start > end
        :raise Overlapping: if the new section overlaps another section
        """
        try:
            index = self.ids.index(id)
        except ValueError:
            raise KeyError()

        new_start = new_start if new_start is not None else self.limits_by_id[id][0]
        new_end = new_end if new_end is not None else self.limits_by_id[id][1]
        if new_color_list is not None:
            if len(new_color_list) != new_end - new_start + 1:
                raise ValueError('length of the color list does not match the new size of the section')
        else:
            color_list = self.color_list_by_id[id]
            new_color_list = [color_list[0]] * (new_end - new_start + 1)

        del self.ids[index]
        del self.color_list[index]
        del self.limits[index]
        del self.is_on [index]
        del self.color_list_by_id[id]
        del self.limits_by_id[id]
        del self.is_on_by_id[id]

        self._insert_section(id, new_start, new_end, new_color_list)

    def new_section(self, start: int, end: int, color: Tuple[int, int, int]) -> str:
        """
        Define a new section

        :raise ValueError: if start > end
        :raise Overlapping: if the new section overlaps another section
        """
        section_id = str(uuid1())
        color_list = [color] * (end - start + 1)
        self._insert_section(section_id, start, end, color_list)
        return section_id

    # noinspection PyShadowingBuiltins
    def set_section_on(self, id: str):
        """
        :raise AlreadyOn: if section is already on
        :raise KeyError: if section do not exist
        """
        if id not in self.ids:
            raise KeyError()
        index = self.ids.index(id)
        self.is_on_by_id[id] = True
        self.is_on.insert(index, True)

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

    # noinspection PyShadowingBuiltins
    def get_section(self, id: str) -> Section:
        """
        Finds and returns a section

        :param id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return Section(id, self.is_on_by_id[id], self.limits_by_id[id], self.color_list_by_id[id])

    def list_sections(self) -> List[Section]:
        """
        Returns all sections ordered by their respective (start, end) limits
        """
        return [
            Section(self.ids[i], self.is_on[i], self.limits[i], self.color_list[i])
            for i in range(len(self.limits))
        ]

    def remove_all_sections(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self.ids = []
        self.color_list = []
        self.limits = []
        self.is_on = []
        self.color_list_by_id = {}
        self.limits_by_id = {}
        self.is_on_by_id = {}

    def remove_sections(self, sections: List[str]):
        """
        Removes sections by id
        :param sections: list of section ids to be removed
        :raise KeyError: if any of the sections in the 'sections' is not defined
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
            raise KeyError(f'section {invalid_section_id} is not defined')


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
        self.strip = PixelStrip(n, pin, freq_hz, dma, invert, brightness, channel)
        self.logger = logging.getLogger(str(self.__class__))
        self.section_manager = SectionManager(config)
        self.is_on = True
        self.strip.begin()

    def new_section(self, start: int, end: int, color: Tuple[int, int, int]) -> str:
        """
        Defines a new section on the strip

        :param start: start position of the section
        :param end: end position of the section
        :param color: color for each led in the section
        :raise ValueError: if start > end
        :raise Overlapping: if the new section overlaps another section
        :return: id of the new section
        """
        return self.section_manager.new_section(start, end, color)

    # noinspection PyShadowingBuiltins
    def edit_section(self, id: str, start: int = None, end: int = None, color_list: List[tuple] = None):
        """
        Changes the start position and/or end position and/or each color of each led of the specified section

        :param id: id of the section that will be edited
        :param start: new start position for the section
        :param end: new end position for the section
        :param color_list: color for each led in the section
        :raises KeyError: if section with section_id is not defined
        :raises ValueError: if limits are defined correctly (also in case of section overlapping)
        """
        return self.section_manager.edit_section(id, start, end, color_list)

    def get_section(self, section_id: str) -> Section:
        """
        Finds and returns a section

        :param section_id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return self.section_manager.get_section(section_id)

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
            new_color_list = [color] * (section.get_limits()[1] - section.get_limits()[0] + 1)
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
        result = []
        sections = self.section_manager.list_sections()
        N = self.strip_length
        S = len(sections)

        if S > 0:
            result = [(0, 0, 0)] * sections[0].get_limits()[0]
            if S > 1:
                for i in range(S - 1):
                    color_list = sections[i].get_color_list()
                    result += color_list if sections[i].is_on() else [(0, 0, 0)] * len(color_list)
                    result += [(0, 0, 0)] * (sections[i + 1].get_limits()[0] - sections[i].get_limits()[1] - 1)
                result += sections[-1].get_color_list()
            else:
                color_list = sections[0].get_color_list()
                result += color_list if sections[0].is_on() else [(0, 0, 0)] * len(color_list)
            result = result + [(0, 0, 0)] * (N - sections[-1].get_limits()[1] - 1)

        return result

    def turn_on(self, section_id: str = None):
        """
        Turns on the entire strip or an specific section

        :raise AlreadyOn: if the strip (or the section) is already on
        :raise KeyError: if section do not exist
        """
        if section_id is None:
            if self.is_on:
                raise AlreadyOn()
            self.is_on = True
        else:
            self.section_manager.set_section_on(section_id)

    def status(self) -> dict:
        return {
            'strip_length': self.strip_length,
            'current_sections': [{
                'id': s.get_id(),
                'is_on': s.is_on(),
                'color': rgb_to_hex(s.get_color_list()[0]),
                'limits': {
                    'start': s.get_limits()[0],
                    'end': s.get_limits()[1]
                }
            } for s in self.section_manager.list_sections()]
        }

    def render(self):
        """
        Renders the actual configuration on the strip
        """
        colors = self. concatenate_sections()
        for i, c in enumerate(colors):
            self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))
        self.strip.show()

    def exec_cmd(self, cmd) -> dict:
        """
        Executes the current command (see set_command) on the current section (see set_section).
        If no section was set, executes the command on the entire strip.

        :return: result of the execution
        """
        cmd.set_controller(self)
        return cmd.exec()
