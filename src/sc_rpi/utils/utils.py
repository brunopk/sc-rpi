"""Generic utility functions."""

from __future__ import annotations

from dataclasses import is_dataclass
from enum import Enum
from typing import Any


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
