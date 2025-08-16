"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from sc_rpi.models.section_resp import SectionResp


@dataclass
class StatusResp:
  """Contains available sections."""

  sections: list[SectionResp]
