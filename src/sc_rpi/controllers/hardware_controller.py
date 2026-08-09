"""Contains the HardwareController class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from rpi_ws281x import Color, PixelStrip

from sc_rpi.controllers.sections_controller import (
    SectionInternalRepresentation,
    SectionsController,
)
from sc_rpi.utils.logging import collapse_multiline_str_into_one_line

if TYPE_CHECKING:
    from sc_rpi.config import Config

_LOGGER = logging.getLogger(__name__)

# TODO: test what happend after removing this @dataclass (it should not be necessary)

# TODO: log all actions (turning on section etc)

@dataclass
class HardwareController:
    """Provides an interface to control the strip (hardware).

    This class is not thread-safe, it cannot be shared between different threads.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the object (constructor).

        Args:
            config (Config): Configurations of SC RPI.

        """
        # Creates sections from config
        _LOGGER.info("Initializing controller")

        self._section_controller = SectionsController(config)
        self._strip_length = config.strip.strip_length

        _LOGGER.info("Initializing PixelStrip instance")
        self._strip = PixelStrip(
            config.strip.strip_length,
            config.strip.pin,
            config.strip.freq_hz,
            config.strip.dma,
            config.strip.invert,
            config.strip.brightness,
            config.strip.channel,
        )
        self._strip.begin()

    def concatenate_sections(self) -> list[tuple]:
        """Concatenates all sections in one list.

        Spaces between section will be filled with Color(0, 0, 0)

        Returns:
            List[tuple]:    List with the length of the strip or void
                            list if no sections are defined

        Raises:
            ApiError:

        """
        result = []
        sections = self._section_controller.list_sections()
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
            result = result + [(0, 0, 0)] * (
                self._strip_length - sections[-1].limits[1] - 1
            )

        return result

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
            start (int | None, optional): New start position for the section. Defaults \
                to None.
            end (int | None, optional): New end position for the section. Defaults to
                None.
            color (tuple[int, int, int] | None, optional): Color for each led in the
                section. Defaults to None.

        Raises:
            ApiError:

        """
        return self._section_controller.edit_section(section_id, start, end, color)

    def get_section(self, section_id: str) -> SectionInternalRepresentation:
        """Obtain a section by ID.

        Args:
            section_id (str): Section to find.

        Returns:
            Section: Returns found section or raise an exception.

        Raises:
            ApiError:

        """
        return self._section_controller.get_section(section_id)

    def list_sections(self) -> list[SectionInternalRepresentation]:
        """Return all defined sections.

        Returns:
            list[Section]: All currently available sections in the strip.

        """
        return self._section_controller.list_sections()

    def new_section(
        self,
        section_id: str,
        start: int,
        end: int,
        color: tuple[int, int, int],
    ) -> SectionInternalRepresentation:
        """Define a new section on the strip.

        Args:
            section_id (str): identifies unequivocally the section.
            start (int): Start position of the section.
            end (int): End position of the section.
            color (Tuple[int, int, int]): Color for each led in the section.

        Raises:
            ApiError:

        """
        return self._section_controller.new_section(
            section_id,
            start,
            end,
            color,
            is_on=True,
        )

    def render(self) -> None:
        """Render the actual configuration on the hardware."""
        colors = self.concatenate_sections()
        if len(colors) == 0:
            warning_msg = """Nothing to render, probably sections were not defined
                correctly or reset command was invoked"""
            _LOGGER.warning(collapse_multiline_str_into_one_line(warning_msg))
        else:
            for i, c in enumerate(colors):
                self._strip.setPixelColor(i, Color(c[0], c[1], c[2]))

        self._strip.show()

    def reset(self) -> None:
        """Reset the state of the strip based on configurations."""
        self._section_controller.reset_sections()

    def turn_section_on(
        self,
        section_id: str,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Turn on a section off the strip.

        Args:
            section_id (str): Section of the strip to be turned on.
            color (tuple[int, int, int] | None, optional): Specified section will be \
                turned on with this color.

        Raises:
            ApiError:

        """
        self._section_controller.turn_section_on(section_id, color)

    # TODO: test turning section off (check that all sections remains unchanged)

    def turn_section_off(self, section_id: str) -> None:
        """Turn off a section off the strip.

        Args:
            section_id (str): Section of the strip to be turned off.

        Raises:
            ApiError:

        """
        self._section_controller.turn_section_off(section_id)

