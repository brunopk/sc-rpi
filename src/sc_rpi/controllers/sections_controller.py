"""Contains the `SectionController` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import structlog

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models.section_internal_representation import SectionInternalRepresentation

if TYPE_CHECKING:
    from sc_rpi.config import Config

logger = structlog.getLogger(__name__)

class SectionsController:
    """Used to control sections in the strip.

    Sections are defined by a start and end position in the strip. All led in the same
    section will have the same color.

    """

    def __init__(self, config: Config) -> None:
        """Initialize the object (constructor).

        Args:
            config (Config): SC RPi configuration.

        """
        self._config = config
        self._strip_length = self._config.strip.strip_length
        self._section_ids: list[str] = []
        self._color_list: list[list[tuple[int, int, int]]] = []
        self._limits: list[tuple[int, int]] = []
        self._is_on: list[bool] = []
        self._names: list[str] = []
        self._color_list_by_id: dict[str, list[tuple[int, int, int]]] = {}
        self._limits_by_id: dict[str, tuple[int, int]] = {}
        self._is_on_by_id: dict[str, bool] = {}
        self._name_by_id: dict[str, str] = {}

        self._initialize_sections()

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
        name = self._name_by_id[section_id]
        new_start = start if start is not None else self._limits_by_id[section_id][0]
        new_end = end if end is not None else self._limits_by_id[section_id][1]
        if color is not None:
            new_color_list = [color] * (new_end - new_start + 1)
        else:
            color_list = self._color_list_by_id[section_id]
            new_color_list = [color_list[0]] * (new_end - new_start + 1)

        del self._section_ids[index]
        del self._color_list[index]
        del self._limits[index]
        del self._is_on[index]
        del self._names[index]
        del self._color_list_by_id[section_id]
        del self._limits_by_id[section_id]
        del self._is_on_by_id[section_id]
        del self._name_by_id[section_id]

        self._insert_section(
            section_id,
            new_start,
            new_end,
            new_color_list,
            is_on=is_on,
            name=name,
        )

    def get_section(self, section_id: str) -> SectionInternalRepresentation:
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
        return SectionInternalRepresentation(
            section_id,
            self._limits_by_id[section_id],
            self._color_list_by_id[section_id],
            self._is_on_by_id[section_id],
            self._name_by_id[section_id],
        )

    def list_sections(self) -> list[SectionInternalRepresentation]:
        """Return all sections ordered by their respective (start, end) limits."""
        return [
            SectionInternalRepresentation(
                self._section_ids[i],
                self._limits[i],
                self._color_list[i],
                is_on=self._is_on[i],
                name=self._names[i],
            )
            for i in range(len(self._limits))
        ]

    def new_section(
        self,
        section_id: str,
        start: int,
        end: int,
        color: tuple[int, int, int] | None = None,
        *_args: object,
        is_on: bool,
        name: str | None = None,
    ) -> SectionInternalRepresentation:
        """Define a new section.

        Args:
            section_id (str): identifies unequivocally the section.
            start (int): Start position.
            end (int): End position.
            color (tuple[int, int, int] | None, optional): Color (RGB). Defaults to None
            is_on (bool): Indicates if the section is turned on/off
            name (str | None, optional): Human readable name. Defaults to the id.

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
        section_name = name if name is not None else section_id
        self._insert_section(
            section_id,
            start,
            end,
            color_list,
            is_on=is_on,
            name=section_name,
        )
        return SectionInternalRepresentation(
            section_id,
            (start, end),
            color_list,
            is_on=is_on,
            name=section_name,
        )

    def replace_sections(self, sections: list[SectionInternalRepresentation]) -> None:
        """Replace all sections with already validated ones.

        It only assigns values, so it cannot fail half way. The sections must come from
        a successful build (see `HardwareController.prepare_config`).

        Args:
            sections (list[SectionInternalRepresentation]): New sections, ordered by
                their start limit.

        """
        self._section_ids = [s.id for s in sections]
        self._color_list = [list(s.color_list) for s in sections]
        self._limits = [s.limits for s in sections]
        self._is_on = [s.is_on for s in sections]
        self._names = [s.name for s in sections]
        self._color_list_by_id = dict(zip(self._section_ids, self._color_list))
        self._limits_by_id = dict(zip(self._section_ids, self._limits))
        self._is_on_by_id = dict(zip(self._section_ids, self._is_on))
        self._name_by_id = dict(zip(self._section_ids, self._names))

    def reset_sections(self) -> None:
        """Reset the state of the strip based on configurations."""
        self._strip_length = self._config.strip.strip_length
        self._section_ids: list[str] = []
        self._color_list: list[list[tuple[int, int, int]]] = []
        self._limits: list[tuple[int, int]] = []
        self._is_on: list[bool] = []
        self._names: list[str] = []
        self._color_list_by_id: dict[str, list[tuple[int, int, int]]] = {}
        self._limits_by_id: dict[str, tuple[int, int]] = {}
        self._is_on_by_id: dict[str, bool] = {}
        self._name_by_id: dict[str, str] = {}

        self._initialize_sections()

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
        self._is_on[index] = False

    # TODO: add/modify test to see if turning section on with a color is working correctly, for example that it don't modify other sections

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

    def _initialize_sections(self) -> None:
        for section in self._config.strip.sections:
            logger.info(
                "Creating section %s from %d to %d",
                section.id,
                section.start,
                section.end,
            )
            self.new_section(
                section.id,
                section.start,
                section.end,
                (section.color.r, section.color.g, section.color.b),
                is_on=section.is_on,
                name=section.name,
            )

    def _insert_section(
        self,
        section_id: str,
        start: int,
        end: int,
        color_list: list[tuple[int, int, int]],
        *_arg: str,
        is_on: bool,
        name: str = "",
    ) -> None:
        if end < start or start < 0 or end >= self._strip_length:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "end < start or start < 0 or end >= strip_length",
            )
        # Ranges are inclusive, so sharing a single led is also an overlap
        for existing_start, existing_end in self._limits:
            if start <= existing_end and existing_start <= end:
                raise ApiError(HTTPStatus.CONFLICT, ErrorCode.SECTION_OVERLAPPING)

        # Counts how many sections start before the new one, which is its position in
        # the lists (they are sorted by start).
        index = sum(1 for existing_start, _ in self._limits if existing_start < start)

        self._is_on.insert(index, is_on)
        self._section_ids.insert(index, section_id)
        self._names.insert(index, name)
        self._color_list.insert(index, color_list)
        self._color_list_by_id[section_id] = color_list
        self._limits.insert(index, (start, end))
        self._limits_by_id[section_id] = (start, end)
        self._is_on_by_id[section_id] = is_on
        self._name_by_id[section_id] = name
