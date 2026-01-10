"""Contains the `SectionController` class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Optional

from sc_rpi.controllers.section import Section
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError

if TYPE_CHECKING:
    from sc_rpi.models.config import Config
    from sc_rpi.models.config.strip_config import StripConfig

LOGGER = logging.getLogger(__name__)

class SectionController:
    """Used to control sections in the strip.

    Sections are defined by a start and end position in the strip. All led in the same
    section will have the same color.

    """

    def __init__(self, config: Config) -> None:
        """Initialize the object (constructor).

        Args:
            config (Config): SC RPi configuration.

        """
        LOGGER.info("Initializing controller")
        self._strip_length = config.strip_config.strip_length
        self._config = config
        self._section_ids: list[str] = []
        self._color_list: list[list[tuple[int, int, int]]] = []
        self._limits: list[tuple[int, int]] = []
        self._is_on: list[bool] = []
        self._color_list_by_id: dict[str, list[tuple[int, int, int]]] = {}
        self._limits_by_id: dict[str, tuple[int, int]] = {}
        self._is_on_by_id: dict[str, bool] = {}
        self._init_sections(config.strip_config)

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
            color (tuple[int, int, int] | None, optional): New color (RGB).

        Raises:
            ApiError:

        """
        try:
            index = self._section_ids.index(section_id)
        except ValueError as ex:
            raise ApiError(
                status=HTTPStatus.NOT_FOUND,
                code=ErrorCode.SECTION_NOT_FOUND,
            ) from ex

        is_on = self._is_on_by_id[section_id]
        new_start = start if start is not None else self._limits_by_id[section_id][0]
        new_end = end if end is not None else self._limits_by_id[section_id][1]
        if color is not None:
            new_color_list = [color] * (new_end - new_start + 1)
        else:
            color_list = self._color_list_by_id[section_id]
            new_color_list = [color_list[0]] * (new_end - new_start + 1)

        # TODO: test if setting color is working correctly

        del self._section_ids[index]
        del self._color_list[index]
        del self._limits[index]
        del self._is_on[index]
        del self._color_list_by_id[section_id]
        del self._limits_by_id[section_id]
        del self._is_on_by_id[section_id]

        self._insert_section(
            section_id,
            new_start,
            new_end,
            new_color_list,
            is_on=is_on,
        )

    def get_section(self, section_id: str) -> Section:
        """Obtain a section by ID.

        Args:
            section_id (str): Section to find.

        Returns:
            Section: Returns found section or raise an exception.

        Raises:
            ApiError:

        """
        if section_id not in self._section_ids:
            raise ApiError(HTTPStatus.NOT_FOUND, ErrorCode.SECTION_NOT_FOUND)
        return Section(
            section_id,
            self._limits_by_id[section_id],
            self._color_list_by_id[section_id],
            self._is_on_by_id[section_id],
        )

    def list_sections(self) -> list[Section]:
        """Return all sections ordered by their respective (start, end) limits."""
        return [
            Section(
                self._section_ids[i],
                self._limits[i],
                self._color_list[i],
                is_on=self._is_on[i],
            )
            for i in range(len(self._limits))
        ]

    def new_section(
        self,
        section_id: str,
        start: int,
        end: int,
        color: Optional[tuple[int, int, int]] = None,
        *_args: object,
        is_on: bool,
    ) -> Section:
        """Define a new section.

        Args:
            section_id (str): identifies unequivocally the section.
            start (int): Start position.
            end (int): End position.
            color (tuple[int, int, int] | None, optional): Color (RGB). Defaults to None
            is_on (bool): Indicates if the section is turned on/off

        Raises:
            ApiError:

        Returns:
            Section: Created section.

        """
        color_list = (
            [color] * (end - start + 1)
            if color is not None
            else [(0, 0, 0)] * (end - start + 1)
        )
        self._insert_section(section_id, start, end, color_list, is_on=is_on)
        return Section(section_id, (start, end), color_list, is_on=is_on)

    def remove_all_sections(self) -> None:
        """Remove all sections."""
        self._section_ids = []
        self._color_list = []
        self._limits = []
        self._is_on = []
        self._color_list_by_id = {}
        self._limits_by_id = {}
        self._is_on_by_id = {}

    def remove_sections(self, sections: list[str]) -> None:
        """Remove a set of sections.

        Args:
            sections (list[str]): Identifiers of the sections to be removed.

        Raises:
            ApiError:

        """
        # test if all sections are defined
        invalid_section_id = None
        for section_id in sections:
            if section_id not in self._limits_by_id:
                invalid_section_id = section_id
                break
        # remove sections (if all sections are defined)
        if invalid_section_id is None:
            for section_id in sections:
                self._remove_section(section_id)
        else:
            raise ApiError(
                HTTPStatus.NOT_FOUND,
                ErrorCode.SECTION_NOT_FOUND,
                message=f"section {invalid_section_id} is not defined",
            )

    def turn_section_off(self, section_id: str) -> None:
        """Turn a section off.

        Args:
            section_id (str): Section to be turned on.

        Raises:
            ApiError:

        """
        if section_id not in self._section_ids:
            raise ApiError(
                status=HTTPStatus.NOT_FOUND,
                code=ErrorCode.SECTION_NOT_FOUND,
            )

        index = self._section_ids.index(section_id)
        self._is_on_by_id[section_id] = False
        self._is_on.insert(index, False)

    # TODO: add/modify test to see if turning section on with a color is working correctly

    def turn_section_on(
        self,
        section_id: str,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Turn a section on.

        Args:
            section_id (str): Section to be turned on.
            color (tuple[int, int, int] | None, optional): Color for all leds in the \
                section.

        Raises:
            ApiError:

        """
        if section_id not in self._section_ids:
            raise ApiError(
                status=HTTPStatus.NOT_FOUND,
                code=ErrorCode.SECTION_NOT_FOUND,
            )

        section_index = self._section_ids.index(section_id)

        if color is not None:
            for color_index, _ in enumerate(self._color_list_by_id[section_id]):
                self._color_list[section_index][color_index] = color
                self._color_list_by_id[section_id][color_index] = color

            self._is_on[section_index] = True
            self._is_on_by_id[section_id] = True
        else:
            for section_index, section_id in enumerate(self._section_ids):
                self._is_on[section_index] = True
                self._is_on_by_id[section_id] = True

    def _insert_section(
        self,
        section_id: str,
        start: int,
        end: int,
        color_list: list[tuple[int, int, int]],
        *_arg: str,
        is_on: bool,
    ) -> None:
        index = None
        if end < start or start < 0 or end >= self._strip_length:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "end < start or start < 0 or end >= strip_length",
            )
        for i, v in enumerate(self._limits):
            if v[0] < start < v[1] or v[0] < end < v[1]:
                raise ApiError(HTTPStatus.CONFLICT, ErrorCode.SECTION_OVERLAPPING)
            if i < len(self._limits) - 1:
                if self._limits[i][0] < start and end < self._limits[i + 1][0]:
                    index = i + 1
                    break
            elif index is None:
                index = i + 1 if start > self._limits[i][1] else i
        index = 0 if index is None else index

        self._is_on.insert(index, True)
        self._section_ids.insert(index, section_id)
        self._color_list.insert(index, color_list)
        self._color_list_by_id[section_id] = color_list
        self._limits.insert(index, (start, end))
        self._limits_by_id[section_id] = (start, end)
        self._is_on_by_id[section_id] = is_on

    def _remove_section(self, section_id: str) -> None:
        section_limits = self._limits_by_id[section_id]
        index = self._limits.index(section_limits)

        del self._section_ids[index]
        del self._color_list[index]
        del self._limits[index]
        del self._is_on[index]
        del self._color_list_by_id[section_id]
        del self._limits_by_id[section_id]
        del self._is_on_by_id[section_id]

    def _init_sections(self, strip_config: StripConfig) -> None:
        for section in strip_config.sections:
            LOGGER.info(
                "Initializing controller, creating section %s from %d to %d",
                section.id,
                section.start,
                section.end,
            )
            self.new_section(
                section.id,
                section.start,
                section.end,
                is_on=False,
            )
