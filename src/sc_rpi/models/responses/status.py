"""Contains the `Status` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .section import Section


@dataclass
class Status:
  """Contains available sections."""

  sections: list[Section]
