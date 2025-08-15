"""Contains `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from sc_rpi.models.responses import Section

@dataclass
class StatusResp:
  """Response for the `status` command."""

  sections: list[Section]
