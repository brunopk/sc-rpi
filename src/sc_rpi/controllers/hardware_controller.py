"""Contains the HardwareController class."""

from __future__ import annotations

from dataclasses import dataclass, replace
from http import HTTPStatus
from typing import TYPE_CHECKING

import structlog
from rpi_ws281x import Color, PixelStrip

from sc_rpi.config.strip import Section
from sc_rpi.controllers.sections_controller import (
    SectionInternalRepresentation,
    SectionsController,
)
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color as ConfigColor
from sc_rpi.utils.config.store import DEFAULT_NAME
from sc_rpi.utils.logging import collapse_multiline_str_into_one_line

if TYPE_CHECKING:
    from sc_rpi.config import Config

logger = structlog.getLogger(__name__)

# TODO: test what happend after removing this @dataclass (it should not be necessary)

# TODO: log all actions (turning on section etc)


def _concatenate_sections(
    sections: list[SectionInternalRepresentation],
    strip_length: int,
) -> list[tuple]:
    """Concatenate sections in one list of colors, one per led of the strip.

    Pure function: it does not read or change any controller state, so it can be used
    on sections that are not (yet) the live ones. Spaces between sections are filled
    with (0, 0, 0).

    Args:
        sections (list[SectionInternalRepresentation]): Sections ordered by start.
        strip_length (int): Number of leds in the strip.

    Returns:
        list[tuple]: List with the length of the strip, or an empty list if there are
            no sections.

    """
    result = []
    number_of_sections = len(sections)
    if number_of_sections > 0:
        result = [(0, 0, 0)] * sections[0].limits[0]
        if number_of_sections > 1:
            for i in range(number_of_sections - 1):
                color_list = sections[i].color_list
                result += (
                    color_list if sections[i].is_on else [(0, 0, 0)] * len(color_list)
                )
                result += [(0, 0, 0)] * (
                    sections[i + 1].limits[0] - sections[i].limits[1] - 1
                )
            color_list = sections[-1].color_list
            result += (
                color_list if sections[-1].is_on else [(0, 0, 0)] * len(color_list)
            )
        else:
            color_list = sections[0].color_list
            result += color_list if sections[0].is_on else [(0, 0, 0)] * len(color_list)
        result = result + [(0, 0, 0)] * (strip_length - sections[-1].limits[1] - 1)

    return result


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
        logger.info("Initializing controller")

        self._config = config
        self._section_controller = SectionsController(config)
        self._strip_length = config.strip.strip_length
        self._description = config.description
        self._active_configuration = DEFAULT_NAME

        logger.info("Initializing PixelStrip instance")
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

    def apply_prepared(
        self,
        sections: list[SectionInternalRepresentation],
        description: str,
        active_configuration: str,
    ) -> None:
        """Render prepared sections and then replace the state.

        The strip is rendered first, from the given sections. Only if that raised no
        exception is the state replaced (a plain in-memory assignment), so a failure
        leaves the sections, the description and the active configuration unchanged.
        It must be the last call of a command, in place of `render()`.

        Args:
            sections (list[SectionInternalRepresentation]): Result of `prepare_config`.
            description (str): Description of the applied configuration.
            active_configuration (str): Name of the applied configuration.

        """
        self._render(_concatenate_sections(sections, self._strip_length))
        self._section_controller.replace_sections(sections)
        self._description = description
        self._active_configuration = active_configuration

    def concatenate_sections(self) -> list[tuple]:
        """Concatenates all sections in one list.

        Spaces between section will be filled with Color(0, 0, 0)

        Returns:
            List[tuple]:    List with the length of the strip or void
                            list if no sections are defined

        Raises:
            ApiError:

        """
        return _concatenate_sections(
            self._section_controller.list_sections(),
            self._strip_length,
        )

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

    def get_active_configuration(self) -> str:
        """Return the name of the active configuration.

        It is the name of the config last loaded by `use_config` or a named `reset`
        (`default` after startup), and the one `reset` without a name reloads.
        """
        return self._active_configuration

    def get_current_config(self) -> Config:
        """Return the initial configuration with the live sections and description.

        Changes made by earlier commands (`edit_section`, `turn_section_off`,
        `use_config`...) are included.

        Returns:
            Config: A new `Config`; the initial `Config` is not modified.

        """
        sections = [
            Section(
                color=ConfigColor(*s.color_list[0]),
                end=s.limits[1],
                id=s.id,
                is_on=s.is_on,
                name=s.name,
                start=s.limits[0],
            )
            for s in self._section_controller.list_sections()
        ]
        strip = replace(self._config.strip, sections=sections)
        return replace(self._config, strip=strip, description=self._description)

    def get_description(self) -> str:
        """Return the description of the running configuration."""
        return self._description

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

    def prepare_config(self, loaded: Config) -> list[SectionInternalRepresentation]:
        """Build the sections of `loaded` without changing any state.

        Sections are validated against the **running** strip length (the hardware
        settings of `loaded` are not applied).

        Args:
            loaded (Config): Configuration to prepare.

        Raises:
            ApiError: With code `INVALID_CONFIG` if the sections are not valid (for
                example overlapping, or beyond the strip length).

        Returns:
            list[SectionInternalRepresentation]: Built sections, ordered by start.

        """
        candidate = replace(
            loaded,
            strip=replace(loaded.strip, strip_length=self._strip_length),
        )
        try:
            return SectionsController(candidate).list_sections()
        except ApiError as ex:
            raise ApiError(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ErrorCode.INVALID_CONFIG,
                ex.message,
            ) from ex

    def render(self) -> None:
        """Render the actual configuration on the hardware."""
        self._render(self.concatenate_sections())

    def reset(self) -> None:
        """Reset the state of the strip based on configurations."""
        self._section_controller.reset_sections()

    # TODO: test turning section off (check that all sections remains unchanged)

    def turn_section_off(self, section_id: str) -> None:
        """Turn off a section off the strip.

        Args:
            section_id (str): Section of the strip to be turned off.

        Raises:
            ApiError:

        """
        self._section_controller.turn_section_off(section_id)

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

    def _render(self, colors: list[tuple]) -> None:
        """Write one color per led to the strip and show it.

        Unlike `render`, it takes the colors to write instead of reading the live
        sections, and it does not change the controller state.

        Args:
            colors (list[tuple]): One (r, g, b) color per led of the strip.

        """
        if len(colors) == 0:
            warning_msg = """Nothing to render, probably sections were not defined
                correctly or reset command was invoked"""
            logger.warning(collapse_multiline_str_into_one_line(warning_msg))
        else:
            for i, c in enumerate(colors):
                self._strip.setPixelColor(i, Color(c[0], c[1], c[2]))

        self._strip.show()
