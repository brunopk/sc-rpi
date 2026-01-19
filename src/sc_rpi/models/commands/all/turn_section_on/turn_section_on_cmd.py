"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.commands.all.turn_section_on.turn_section_on_args import (
    TurnSectionOnArgs,
)
from sc_rpi.models.commands.all.turn_section_on.turn_section_on_sc_rpi_result import (
    TurnSectionOnScRpiResult,
)
from sc_rpi.models.commands.command import Command, CommandResult
from sc_rpi.models.commands.command_result.status import Status
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.mappings import map_sections
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_state_topic,
)

# TODO: if section is not modify, do not return any message to HA

@dataclass
class TurnSectionOnCmd(Command[TurnSectionOnArgs]):
    """`turn_section_on` command."""

    args: TurnSectionOnArgs

    name: str = "turn_section_on"

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        color = (
            (self.args.color.r, self.args.color.g, self.args.color.b)
            if self.args.color is not None
            else None
        )

        self._hw_controller.turn_section_on(self.args.section_id, color)

        sections = self._hw_controller.list_sections()
        sc_rpi_result_payload = Status(map_sections(sections))
        sc_rpi_result = TurnSectionOnScRpiResult(
            HTTPStatus.ACCEPTED,
            TurnSectionOnCmd.name,
            sc_rpi_result_payload,
        )

        """
        Setting the correct brightness is not implemented (it just returns what \
            receives)
        """
        turned_on_section = self._hw_controller.get_section(self.args.section_id)
        ha_entity_state = HAState(
            State.ON,
            brightness=self.args.brightness,
            color=self.args.color,
            color_mode=ColorMode.RGB,
        )
        ha_entity_state_topic = build_ha_state_topic(turned_on_section.id)

        self._hw_controller.render()

        return {
            SC_RPI_RESULT_TOPIC: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }
