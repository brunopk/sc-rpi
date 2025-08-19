"""Contains the `HelpRespPayload` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HelpRespPayload:
    """Contain helpful information for users."""

    commands: list[str]
