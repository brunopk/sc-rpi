"""Contains the `SectionEdit` class."""
from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.edit_section.edit_section_args import EditSectionArgs
from sc_rpi.commands.edit_section.edit_section_sc_rpi_result import (
    EditSectionScRpiResult,
)
from sc_rpi.models.command.command import Command, CommandResult
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.mappings import map_sections

# TODO: return the correct object for each MQTT topic

@dataclass
class EditSectionCmd(Command[EditSectionArgs]):
    """`edit_section` command."""

    args: EditSectionArgs

    name: str = "edit_section"

    @log_call()
    def run(self) -> CommandResult:
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
        status = Status(map_sections(sections))

        return EditSectionScRpiResult(HTTPStatus.ACCEPTED, EditSectionCmd.name, status)
