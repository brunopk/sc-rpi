"""Contains the `TurnSectionOffCmd` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.turn_section_off.args import TurnSectionOffArgs
from sc_rpi.enums.homeassistant import State
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.results import build_status_result
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC, build_ha_state_topic

_LOGGER = logging.getLogger(__name__)


@dataclass
class TurnSectionOffCmd(Command[TurnSectionOffArgs]):
    """`turn_section_off` command."""

    command_args: TurnSectionOffArgs

    command_name: str = "turn_section_off"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_section_off(self.command_args.section_id)

        # TODO: test what happens if color and color mode is not sent to Home assistant

        section_id = self.command_args.section_id
        section_to_be_turned_off = self._hw_controller.get_section(section_id)

        ha_entity_state_topic = build_ha_state_topic(self.command_args.section_id)
        ha_entity_state = HAState(State.OFF, brightness=0)

        sc_rpi_result = build_status_result(
            self._hw_controller,
            self.command_name,
        )

        if section_to_be_turned_off.is_on:
            _LOGGER.warning(
                "Trying to turn section already off section (section_id={%s})",
                section_id,
            )

        self._hw_controller.render()

        return {
            SC_RPI_RESULT_TOPIC: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }
