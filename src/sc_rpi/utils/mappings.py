"""Contains functions to map between different objects."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.results import Error, Result, Section
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models.color import Color

if TYPE_CHECKING:
    from sc_rpi.commands.base import Command
    from sc_rpi.models.section_internal_representation import (
        SectionInternalRepresentation,
    )

def map_section_list(
    section_list: list[SectionInternalRepresentation],
) -> list[Section]:
    """Convert a `Section` instances to `results.Section` instances.

    Args:
        section_list (list[Section]): Section list. All entries in the section are
            assumed to have the same color.

    Returns:
        list[responses.Section]: The converted list

    """
    return [
        Section(
            section.id,
            section.limits[0],
            section.limits[1],
            Color(
                section.color_list[0][0],
                section.color_list[0][1],
                section.color_list[0][2],
            ),
            section.is_on,
        )
        for section in section_list
    ]

def map_color_to_ha_format(color: tuple[int, int, int]) -> str:
    """Map a color to required format for RGB color state topic for Home Assistant.

    Args:
        color (tuple[int, int, int]): Color to be mapped (RBG)

    """
    return str(color)[1:-1].replace(" ", "")

def map_exception(ex: Exception, command: Command | None) -> Result:
    """Map any exception to a `Result`.

    Args:
        ex (Exception): Exception to be mapped. It may be an `ApiError.`
        command (Command): Command that caused the exception. Use this parameter if \
            the exception was caused by a command.

    Returns:
        ScRpiBaseResult: Object that can be send through an MQTT topic.

    """
    command_name = command.command_name if command is not None else None
    return (
        Result(ex.status, command_name, error=Error(ex.code, ex.code.name))
        if isinstance(ex, ApiError)
        else Result(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            command_name,
            error=Error(
                ErrorCode.INTERNAL_SERVER_ERROR,
                ErrorCode.INTERNAL_SERVER_ERROR.name,
            ),
        )
    )
