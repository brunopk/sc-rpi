"""Contains the `SectionEdit` class."""
from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.edit_section.edit_section_args import EditSectionArgs
from sc_rpi.commands.edit_section.edit_section_sc_rpi_result import (
    EditSectionScRpiResult,
)
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.command.command import Command, CommandResult
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.mappings import map_sections
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_state_topic,
)


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

        sections = self._hw_controller.list_sections()
        sc_rpi_result_payload = Status(map_sections(sections))
        sc_rpi_result = EditSectionScRpiResult(
            HTTPStatus.ACCEPTED,
            EditSectionCmd.name,
            sc_rpi_result_payload,
        )

        result = {SC_RPI_RESULT_TOPIC: sc_rpi_result }

        modified_section = self._hw_controller.get_section(self.args.section_id)
        is_color_modified = (
            color is not None and modified_section.color_list[0] != color
        )
        if is_color_modified:
            ha_entity_state = HAState(
                State.ON,
                color=self.args.color,
                color_mode=ColorMode.RGB,
            )
            ha_entity_state_topic = build_ha_state_topic(modified_section.id)
            result[ha_entity_state_topic] = ha_entity_state

        self._hw_controller.render()

        return result
