"""Contains the `SectionEdit` class."""
from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.edit_section.args import EditSectionArgs
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.results import build_sc_rpi_status_result
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_state_topic,
)


@dataclass
class EditSection(Command[EditSectionArgs]):
    """`edit_section` command."""

    command_args: EditSectionArgs

    command_name: str = "edit_section"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        color = (
            (
                self.command_args.color.r,
                self.command_args.color.g,
                self.command_args.color.b,
            )
            if self.command_args.color is not None
            else None
        )
        self._hw_controller.edit_section(
            self.command_args.section_id,
            self.command_args.start,
            self.command_args.end,
            color,
        )

        sc_rpi_result = build_sc_rpi_status_result(
            self._hw_controller,
            self.command_name,
        )
        result = {SC_RPI_RESULT_TOPIC: sc_rpi_result }

        modified_section = self._hw_controller.get_section(self.command_args.section_id)
        is_color_modified = (
            color is not None and modified_section.color_list[0] != color
        )
        if is_color_modified:
            ha_entity_state = HAState(
                State.ON,
                color=self.command_args.color,
                color_mode=ColorMode.RGB,
            )
            ha_entity_state_topic = build_ha_state_topic(modified_section.id)
            result[ha_entity_state_topic] = ha_entity_state

        self._hw_controller.render()

        return result
