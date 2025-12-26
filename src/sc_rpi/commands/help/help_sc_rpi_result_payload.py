"""Contains the `HelpRespPayload` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HelpScRpiResultPayload:
    """Contain helpful information for users."""

    commands: list[str]
