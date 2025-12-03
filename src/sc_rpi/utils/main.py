"""Generic utility functions."""

from __future__ import annotations

from dataclasses import is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

from sc_rpi.models import SectionAux
from sc_rpi.models.color import Color

if TYPE_CHECKING:
    from sc_rpi.controllers import Section

MAX_RGB = 255

def is_valid_color(color: tuple[int, int, int]) -> bool:
    """Validate a color.

    Args:
        color (str): Color in hex notation.

    Returns:
        bool: Returns `True` if it's a valid color. Otherwise, returns `False`

    """
    return (
        0 <= color[0] <= MAX_RGB
        and 0 <= color[1] <= MAX_RGB
        and 0 <= color[2] <= MAX_RGB
    )


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


def to_dict(obj: Any) -> dict | list | str:
    """Convert any `@dataclass` decorated object into a dict.

    All enum values will be serialized into string.

    Args:
        obj (Any): Object to be mapped.

    Returns:
        dict | list | str: Returns the converted object.

    """
    if is_dataclass(obj):
        result = {}
        for k, v in obj.__dict__.items():
            result[k] = to_dict(v)
        return result
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_dict(i) for i in obj]
    if isinstance(obj, Enum):
        return obj.name

    return obj
