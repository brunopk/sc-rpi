"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HelpResp:
    """Contain helpful information for users."""

    commands: list[str]
