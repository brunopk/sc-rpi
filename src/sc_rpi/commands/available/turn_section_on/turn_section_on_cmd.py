"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.commands.available.turn_section_on.turn_section_on_args import (
    TurnSectionOnArgs,
)
from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.commands.results import build_sc_rpi_status_result
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_state_topic,
)

# TODO: if section is not modify, do not return any message to HA

@dataclass
class TurnSectionOnCmd(Command[TurnSectionOnArgs]):
    """`turn_section_on` command."""

    command_args: TurnSectionOnArgs

    command_name: str = "turn_section_on"

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

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

        self._hw_controller.turn_section_on(self.command_args.section_id, color)

        """
        Setting the correct brightness is not implemented (it just returns what \
            receives)
        """
        turned_on_section = self._hw_controller.get_section(self.command_args.section_id)
        ha_entity_state = HAState(
            State.ON,
            brightness=self.command_args.brightness,
            color=self.command_args.color,
            color_mode=ColorMode.RGB,
        )
        ha_entity_state_topic = build_ha_state_topic(turned_on_section.id)
        sc_rpi_result = build_sc_rpi_status_result(self._hw_controller, self.command_name)

        self._hw_controller.render()

        return {
            SC_RPI_RESULT_TOPIC: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }
