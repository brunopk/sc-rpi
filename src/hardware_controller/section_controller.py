"""Contains the SectionController class."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple
from uuid import uuid1

from enums import ErrorCode
from errors import ApiError
from models import Section

if TYPE_CHECKING:
    from configparser import ConfigParser

# TODO: CONTINUE CHECK ALL METHODS

class SectionController:
    """Used to control sections in the strip."""

    def __init__(self, config: ConfigParser) -> None:
        """Initialize the SectionController.

        Args:
            config (ConfigParser): Necessary to obtain strip properties.

        """
        self._strip_length = int(config['PIXEL_STRIP'].get('n'))
        self._config = config
        self._section_ids: list[str] = []
        self._color_list: list[list[tuple[int, int, int]]] = []
        self._limits: list[tuple[int, int]] = []
        self._is_on: list[bool] = []
        self._color_list_by_id: dict[str, str] = {}
        self._limits_by_id: dict[str, tuple[int, int]] = {}
        self._is_on_by_id: dict[str, bool] = {}

    def edit_section(
        self,
        section_id: str,
        start: int | None = None,
        end: int | None = None,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Edits a section.

        Args:
            section_id (str): Identifies the section.
            start (int | None, optional): New start position.
            end (int | None, optional): New end position.
            color (tuple[int, int, int] | None, optional): New color.


        Raises:
            KeyError: If section not exist
            ValueError: If start > end
            Overlapping: If the new section overlaps another section

        """
        try:
            index = self.ids.index(id)
        except ValueError as ex:
            raise KeyError from ex

        new_start = start if start is not None else self.limits_by_id[id][0]
        new_end = end if end is not None else self.limits_by_id[id][1]
        if color is not None:
            new_color_list = [color] * (new_end - new_start + 1)
        else:
            color_list = self.color_list_by_id[id]
            new_color_list = [color_list[0]] * (new_end - new_start + 1)

        del self._section_ids[index]
        del self._color_list[index]
        del self._limits[index]
        del self.is_on[index]
        del self._color_list_by_id[section_id]
        del self._limits_by_id[section_id]
        del self._is_on_by_id[section_id]

        self._insert_section(section_id, new_start, new_end, new_color_list)

    def new_section(self, start: int, end: int, color: tuple[int, int, int]) -> str:
        """Define a new section.

        Raises:
            ValueError: if start > end
            Overlapping: if the new section overlaps another section

        """
        section_id = str(uuid1())
        color_list = [color] * (end - start + 1)
        self._insert_section(section_id, start, end, color_list)
        return section_id

    def set_section_on(self, id: str):
        """
        :raise KeyError: if section not exist
        """
        if id not in self.ids:
            raise KeyError()
        index = self.ids.index(id)
        self.is_on_by_id[id] = True
        self.is_on.insert(index, True)

    def set_section_off(self, id: str):
        """
        :raise KeyError: if section do not exist
        """
        if id not in self.ids:
            raise KeyError()
        index = self.ids.index(id)
        self.is_on_by_id[id] = False
        self.is_on.insert(index, False)

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

    def get_section(self, id: str) -> Section:
        """
        Finds and returns a section

        :param id: identifier of the section to look for
        :raises KeyError: if the section is not defined
        """
        return Section(id, self.is_on_by_id[id], self.limits_by_id[id], self.color_list_by_id[id])

    def list_sections(self) -> list[Section]:
        """Return all sections ordered by their respective (start, end) limits."""
        return [
            Section(
                self._section_ids[i],
                self._limits[i],
                self._color_list[i],
                is_on=self._is_on[i],
            )
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

    def _insert_section(self, id: str, start: int, end: int, color_list):
        """
        :raise ApiError: if start > end, start < 0, end >= strip_length or new section overlaps another section
        """
        index = None
        if end < start or start < 0 or end >= self.strip_length:
            raise ApiError(ErrorCode.BAD_REQUEST, 'end < start or start < 0 or end >= strip_length')
        for i, v in enumerate(self.limits):
            if v[0] < start < v[1] or v[0] < end < v[1]:
                raise ApiError(ErrorCode.OVERLAPPING)
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
