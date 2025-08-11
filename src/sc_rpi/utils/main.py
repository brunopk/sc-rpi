"""Generic utility functions."""

from __future__ import annotations

from dataclasses import is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

from webcolors import rgb_to_hex

from sc_rpi.models import responses

if TYPE_CHECKING:
    from sc_rpi.controllers import Section


def map_sections(section_list: list[Section]) -> list[responses.Section]:
    """Convert a `Section` instances to `responses.Section`.

    Args:
        section_list (list[Section]): Section list. All entries in the section are
            assumed to have the same color.

    Returns:
        list[responses.Section]: The converted list

    """
    return [
        responses.Section(
            section.id,
            section.limits[0],
            section.limits[1],
            rgb_to_hex(section.color_list[0]),
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
