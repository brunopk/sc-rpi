"""Contains the HardwareController class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from rpi_ws281x import Color, PixelStrip

from sc_rpi.controllers.section_controller import SectionController

if TYPE_CHECKING:
    from sc_rpi.controllers.section import Section
    from sc_rpi.models.config import Config

logger = logging.getLogger(__name__)

@dataclass
class HardwareController:
    """Provides an interface to control the strip (hardware).

    This class is not thead-safe, it cannot be shared between different threads.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the object (constructor).

        Args:
            config (Config): Configurations of SC RPI.

        """
        logger.debug("Initializing HardwareController instance")
        self._section_controller = SectionController(config)
        logger.debug("Initializing PixelStrip instance")
        self._strip = PixelStrip(
            config.strip_config.strip_length,
            config.strip_config.pin,
            config.strip_config.freq_hz,
            config.strip_config.dma,
            config.strip_config.invert,
            config.strip_config.brightness,
            config.strip_config.channel,
        )
        self._strip_length = config.strip_config.strip_length
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

    def list_sections(self) -> list[Section]:
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
    ) -> Section:
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

    def remove_all_sections(self) -> None:
        """Remove all sections.

        This will reset the whole controller to the state after instantiation.
        """
        self._section_controller.remove_all_sections()

    def remove_sections(self, sections: list[str]) -> None:
        """Remove one or more sections in the strip.

        Args:
            sections (list[str]): Sections to be removed (identified by their IDs)

        Raises:
            ApiError:

        """
        self._section_controller.remove_sections(sections)

    def render(self) -> None:
        """Render the actual configuration on the hardware."""
        colors = self.concatenate_sections()
        if len(colors) == 0:
            logger.warning(
                "Nothing to render, probably sections were not defined correctly",
            )
        else:
            for i, c in enumerate(colors):
                self._strip.setPixelColor(i, Color(c[0], c[1], c[2]))

        self._strip.show()

    def turn_on(
        self,
        section_id: str | None = None,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Turn on the entire strip or an specific section.

        Args:
            section_id (str | None, optional): Use `None` to turn the whole strip on.
            color (tuple[int, int, int] | None, optional): Color for all leds in the \
                section.

        Raises:
            ApiError:

        """
        if section_id is None:
            self._is_on = True
        else:
            self._section_controller.turn_section_on(section_id, color)

    def turn_off(self, section_id: str | None = None) -> None:
        """Turn off the entire strip or an specific section.

        Raises:
            ApiError:

        """
        if section_id is None:
            self._is_on = False
        else:
            self._section_controller.turn_section_off(section_id)

