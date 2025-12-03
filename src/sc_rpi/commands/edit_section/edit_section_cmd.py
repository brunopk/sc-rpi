"""Contains the `SectionEdit` class."""
from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from webcolors import hex_to_rgb

from sc_rpi.commands.edit_section.edit_section_args import EditSectionArgs
from sc_rpi.commands.edit_section.edit_section_resp import EditSectionResp
from sc_rpi.models import StatusRespPayload
from sc_rpi.models.command import Command
from sc_rpi.utils import map_sections


@dataclass
class EditSectionCmd(Command[EditSectionArgs]):
    """`edit_section` command."""

    args: EditSectionArgs

    name: str = "edit_section"

    def run(self) -> EditSectionResp:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        color = (
            (self.args.color.r, self.args.color.g, self.args.color.b)
            if self.args.color is not None
            else None
        )
        self._hw_controller.edit_section(
            self.args.section_id,
            self.args.start,
            self.args.end,
            color,
        )

        self._hw_controller.render()

        sections = self._hw_controller.list_sections()
        payload = StatusRespPayload(map_sections(sections))

        return EditSectionResp(HTTPStatus.ACCEPTED, EditSectionCmd.name, payload)
