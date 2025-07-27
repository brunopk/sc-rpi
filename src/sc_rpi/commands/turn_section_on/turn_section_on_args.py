"""Contains the `TurnSectionOnArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TurnSectionOnArgs:
    """`turn_section_on` command arguments."""

    section_id: str
