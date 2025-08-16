"""Contains the `StatusResp` class."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.section_resp import SectionResp


@dataclass
class StatusResp(DataClassJSONMixin):
  """Contains available sections."""

  sections: list[SectionResp]
