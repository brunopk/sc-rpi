"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.turn_section_on.args import TurnSectionOnArgs
from sc_rpi.enums.homeassistant import ColorMode, State
from sc_rpi.models.color import Color
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.results import build_status_result
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_state_topic,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class TurnSectionOnCmd(Command[TurnSectionOnArgs]):
    """`turn_section_on` command."""

    command_args: TurnSectionOnArgs

    command_name: str = "turn_section_on"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        if self.command_args.color is not None:
            new_color = self.command_args.color
            new_color_as_tuple = (
                self.command_args.color.r,
                self.command_args.color.g,
                self.command_args.color.b,
            )
        else:
            _LOGGER.info("Using default color")
            new_color = Color(0, 0, 0)
            new_color_as_tuple = (0, 0, 0)

        section_id = self.command_args.section_id
        section_to_be_turned_on = self._hw_controller.get_section(section_id)
        previous_color = section_to_be_turned_on.color_list[0]

        self._hw_controller.turn_section_on(
            self.command_args.section_id, new_color_as_tuple
        )

        sc_rpi_result = build_status_result(self._hw_controller, self.command_name)

        """
        Setting the correct brightness is not implemented (it just returns what \
            receives)
        """
        ha_entity_state = HAState(
            State.ON,
            brightness=self.command_args.brightness,
            color=new_color,
            color_mode=ColorMode.RGB,
        )
        ha_entity_state_topic = build_ha_state_topic(section_to_be_turned_on.id)

        if section_to_be_turned_on.is_on and previous_color == new_color:
            _LOGGER.info(
                "Trying to turn on an already on section with the same color (section_id={%s})",
                section_id,
            )

        self._hw_controller.render()

        return {
            SC_RPI_RESULT_TOPIC: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }
