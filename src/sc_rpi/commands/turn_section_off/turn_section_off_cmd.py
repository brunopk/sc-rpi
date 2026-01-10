"""Contains the `TurnSectionOffCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.turn_section_off.turn_section_off_args import TurnSectionOffArgs
from sc_rpi.commands.turn_section_off.turn_section_off_sc_rpi_result import (
    TurnSectionOffScRpiResult,
)
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.command.command import Command, CommandResult
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.mappings import map_sections
from sc_rpi.utils.topic_utils import build_ha_state_topic, build_sc_rpi_result_topic


@dataclass
class TurnSectionOffCmd(Command[TurnSectionOffArgs]):
    """`turn_section_off` command."""

    args: TurnSectionOffArgs

    name: str = "turn_section_off"

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_section_off(self.args.section_id)

        sections = self._hw_controller.list_sections()
        sc_rpi_result_payload = Status(map_sections(sections))
        sc_rpi_result = TurnSectionOffScRpiResult(
            HTTPStatus.ACCEPTED,
            TurnSectionOffCmd.name,
            sc_rpi_result_payload,
        )

        # TODO: test what happens if color and color mode is not sent to Home assistant
        ha_entity_state = HAState(State.OFF, brightness=0)
        ha_entity_state_topic = build_ha_state_topic(self.args.section_id)

        """
        IMPORTANT: rendering strip should be the last thing before returning from the \
            function to avoid rendering anything before any part of the code could \
                raise an exception.
        """
        self._hw_controller.render()

        return {
            self.__sc_rpi_result_topic: sc_rpi_result,
            ha_entity_state_topic: ha_entity_state,
        }

    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        self.__sc_rpi_result_topic = build_sc_rpi_result_topic()

