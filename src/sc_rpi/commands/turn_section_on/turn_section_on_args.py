"""Contains the `TurnSectionOnArgs` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# TODO: CONTINUE: get the color and turn the strip with this color
# TODO: CONTINUE: run all unit test to see if nothing is broken

@dataclass
class TurnSectionOnArgs:
    """`turn_section_on` command arguments."""

    section_id: str

    color: Optional[str] = None

