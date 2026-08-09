"""Contains the `TurnSectionOffArgs` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TurnSectionOffArgs:
    """`turn_section_off` command arguments."""

    section_id: str
