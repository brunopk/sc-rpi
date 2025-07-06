"""Contains the `Status` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .section import Section


@dataclass
class Status:
  """Represent the current status of the system."""

  section: list[Section]
