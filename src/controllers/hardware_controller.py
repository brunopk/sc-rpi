"""Contains the HardwareController class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Tuple

from rpi_ws281x import Color, PixelStrip
from webcolors import rgb_to_hex

from enums import ErrorCode
from errors import ApiError
from helpers import parse_bool

from .section_controller import SectionController

if TYPE_CHECKING:
    from configparser import ConfigParser

    from models import Section

LOGGER = logging.getLogger(__name__)

class HardwareController:
    """Provides an interface to control the strip (hardware)."""

    def __init__(self, config: ConfigParser):
        n = int(config['PIXEL_STRIP'].get('n'))
        pin = int(config['PIXEL_STRIP'].get('pin'))
        freq_hz = int(config['PIXEL_STRIP'].get('freq_hz'))
        dma = int(config['PIXEL_STRIP'].get('dma'))
        invert = parse_bool(config['PIXEL_STRIP'].get('invert'))
        brightness = int(config['PIXEL_STRIP'].get('brightness'))
        channel = int(config['PIXEL_STRIP'].get('channel'))

        if n is None:
            raise Exception('Cannot initialize HardwareController, n was not set in config.ini')
        if pin is None:
            raise Exception('Cannot initialize HardwareController, pin was not set in config.ini')
        if freq_hz is None:
            raise Exception('Cannot initialize HardwareController, freq_hz was not set in config.ini')
        if dma is None:
            raise Exception('Cannot initialize HardwareController, dma was not set in config.ini')
        if invert is None:
            raise Exception('Cannot initialize HardwareController, invert was not set in config.ini')
        if brightness is None:
            raise Exception('Cannot initialize HardwareController, brightness was not set in config.ini')
        if channel is None:
            raise Exception('Cannot initialize HardwareController, channel was not set in config.ini')

        self._section_controller = SectionController(config)
        self.strip_length = n
        self.strip = PixelStrip(n, pin, freq_hz, dma, invert, brightness, channel)
        self.is_on = False
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
        return self._section_controller.new_section(start, end, color)

    def edit_section(
        self,
        section_id: str,
        start: int | None = None,
        end: int | None = None,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Change the start position and/or end position and/or each color of each led \

        of the specified section.

        Args:
            section_id (str): ID of the section that will be edited.
            start (int | None, optional): New start position for the section.Defaults to
                None.
            end (int | None, optional): New end position for the section. Defaults to
                None.
            color (tuple[int, int, int] | None, optional): Color for each led in the
                section. Defaults to None.

        Raises:
            ApiError:

        """
        return self._section_controller.edit_section(section_id, start, end, color)

    def get_section(self, section_id: str) -> Section:
        """
        Finds and returns a section

        :param section_id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return self._section_controller.get_section(section_id)

    def remove_sections(self, sections: list[str]) -> None:
        """Remove one or more sections in the strip.

        Args:
            sections (list[str]): Sections to be removed (identified by their IDs)
        """
        self._section_controller.remove_sections(sections)

    def remove_all_sections(self):
        """
        Removes all sections and resets the current section (see set_current_section) to None
        """
        self._section_controller.remove_all_sections()

    def concatenate_sections(self) -> list[tuple]:
        """Concatenates all sections in one list.

        Spaces between section will be filled with Color(0, 0, 0)

        Returns:
            List[tuple]:    List with the length of the strip or void
                            list if no sections are defined

        """
        result = []
        sections = self._section_controller.list_sections()
        strip_length = self.strip_length
        number_of_sections = len(sections)

        if number_of_sections > 0:
            result = [(0, 0, 0)] * sections[0].limits[0]
            if number_of_sections > 1:
                for i in range(number_of_sections - 1):
                    color_list = sections[i].color_list
                    result += (
                        color_list
                        if sections[i].is_on
                        else [(0, 0, 0)] * len(color_list)
                    )
                    result += [(0, 0, 0)] * (
                        sections[i + 1].limits[0] - sections[i].limits[1] - 1
                    )
                result += sections[-1].color_list
            else:
                color_list = sections[0].color_list
                result += (
                    color_list if sections[0].is_on else [(0, 0, 0)] * len(color_list)
                )
            result = result + [(0, 0, 0)] * (strip_length - sections[-1].limits[1] - 1)

        return result

    def turn_on(self, section_id: str | None = None) -> None:
        """Turn on the entire strip or an specific section.

        Raises:
            ApiError:

        """
        if section_id is None:
            self.is_on = True
        else:
            self._section_controller.turn_section_on(section_id)

    def turn_off(self, section_id: str | None = None) -> None:
        """Turn off the entire strip or an specific section.

        Raises:
            ApiError:

        """
        if section_id is None:
            self.is_on = False
        else:
            self._section_controller.turn_section_off(section_id)

    def status(self) -> dict:
        return {
            'strip_length': self.strip_length,
            'current_sections': [{
                'id': s.id,
                'is_on': s.is_on,
                'color': rgb_to_hex(s.color_list[0]),
                'limits': {
                    'start': s.limits[0],
                    'end': s.limits[1]
                }
            } for s in self._section_controller.list_sections()]
        }

    def render(self):
        """
        Renders the actual configuration on the strip
        """
        colors = self.concatenate_sections()
        if len(colors) == 0 or not self.is_on:
            if len(colors) == 0:
                LOGGER.warning('No sections defined (rendering Color(0, 0, 0))')
            if not self.is_on:
                LOGGER.warning('Strip is turned off (Color(0, 0, 0))')
            for i in range(self.strip_length):
                self.strip.setPixelColor(i, Color(0, 0, 0))
        else:
            for i, c in enumerate(colors):
                self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))

        self.strip.show()
