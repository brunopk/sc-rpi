"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.section_aux import SectionAux

# TODO: rename to ResponsePayload
# TODO: move this into a new models.response package

@dataclass
class StatusRespPayload(DataClassJSONMixin):
  """Contains available sections."""

  sections: list[SectionAux]
