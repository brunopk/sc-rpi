"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.commands.command_result.section_aux import SectionAux


@dataclass
class Status(DataClassJSONMixin):
  """Contains available sections."""

  sections: list[SectionAux]
