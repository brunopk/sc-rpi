"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.results.section_aux import SectionAux

# TODO: move this class to sc_rpi_status_result and rename to StatusPayload


@dataclass
class Status(DataClassJSONMixin):
  """Contains available sections."""

  sections: list[SectionAux]
