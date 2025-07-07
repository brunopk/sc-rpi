"""Contains `Status` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from sc_rpi.models.responses import Client, Section

@dataclass
class Status:
  """Response for the `status` command."""

  sections: list[Section]

  clients: list[Client]
