"""Contains functions to map between different command objects."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.results.sc_rpi_base_result import ScRpiBaseResult
from sc_rpi.commands.results.sc_rpi_error import ScRpiError
from sc_rpi.commands.results.section_aux import SectionAux
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models.color import Color

if TYPE_CHECKING:
    from sc_rpi.commands.base import Command
    from sc_rpi.controllers import Section

def map_sections(section_list: list[Section]) -> list[SectionAux]:
    """Convert a `Section` instances to `responses.Section`.

    Args:
        section_list (list[Section]): Section list. All entries in the section are
            assumed to have the same color.

    Returns:
        list[responses.Section]: The converted list

    """
    return [
        SectionAux(
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

def map_exception_to_sc_rpi_result(
    ex: Exception,
    sc_rpi_command: Command | None,
) -> ScRpiBaseResult:
    """Map any exception into an `ScRpiBaseResult` that can be send through a MQTT \

        topic.

    Args:
        ex (Exception): Exception to be mapped. It may be an `ApiError.`
        sc_rpi_command (Command): Command that caused the exception. Use this \
            parameter if the exception was caused by a command.

    Returns:
        ScRpiBaseResult: Object that can be send through an MQTT topic.

    """
    command_name = sc_rpi_command.command_name if sc_rpi_command is not None else None
    return (
        ScRpiBaseResult(
            ex.status,
            command_name,
            sc_rpi_error=ScRpiError(ex.code, ex.code.name),
        )
        if isinstance(ex, ApiError)
        else ScRpiBaseResult(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            command_name,
            sc_rpi_error=ScRpiError(
                ErrorCode.INTERNAL_SERVER_ERROR,
                ErrorCode.INTERNAL_SERVER_ERROR.name,
            ),
        )
    )
