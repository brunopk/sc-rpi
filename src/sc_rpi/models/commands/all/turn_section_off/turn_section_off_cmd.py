"""Contains the `TurnSectionOffCmd` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.commands.all.turn_section_off.turn_section_off_args import (
    TurnSectionOffArgs,
)
from sc_rpi.models.commands.command import Command, CommandResult
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.command_result import build_sc_rpi_status_result
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC, build_ha_state_topic


@dataclass
class TurnSectionOffCmd(Command[TurnSectionOffArgs]):
    """`turn_section_off` command."""

    command_args: TurnSectionOffArgs

    command_name: str = "turn_section_off"

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_section_off(self.command_args.section_id)

        # TODO: test what happens if color and color mode is not sent to Home assistant

        sc_rpi_result = build_sc_rpi_status_result(
            self._hw_controller,
            self.command_name,
        )
        ha_entity_state = HAState(State.OFF, brightness=0)
        ha_entity_state_topic = build_ha_state_topic(self.command_args.section_id)

        # TODO: move this comment to a .md file (documentation)

        """
        IMPORTANT: rendering strip should be the last thing before returning from the \
            function to avoid rendering anything before any part of the code could \
                raise an exception.
        """
        self._hw_controller.render()

        return {
            SC_RPI_RESULT_TOPIC: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }
