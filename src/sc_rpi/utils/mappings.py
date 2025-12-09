"""Contains functions to map between different command objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sc_rpi.models.color import Color
from sc_rpi.models.response.section_aux import SectionAux

if TYPE_CHECKING:
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

