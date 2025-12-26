"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.turn_section_on.turn_section_on_args import TurnSectionOnArgs
from sc_rpi.commands.turn_section_on.turn_section_on_sc_rpi_result import (
    TurnSectionOnScRpiResult,
)
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.state import State
from sc_rpi.models.command.command import Command
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.models.homeassistant.ha_state import HAState
from sc_rpi.utils.mappings import map_sections
from sc_rpi.utils.topic_utils import (
    build_ha_state_topic,
    build_sc_rpi_result_topic,
)


@dataclass
class TurnSectionOnCmd(Command[TurnSectionOnArgs]):
    """`turn_section_on` command."""

    args: TurnSectionOnArgs

    name: str = "turn_section_on"

    def run(self) -> dict[str, DataClassJSONMixin | str]:
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

        turned_on_section = self._hw_controller.get_section(self.args.section_id)
        ha_entity_state = (
            HAState(
                State.ON,
                brightness=self.args.brightness,
                color=self.args.color,
                color_mode=ColorMode.RGB,
            )
            if turned_on_section.is_on
            else HAState(State.OFF, brightness=self.args.brightness)
        )
        ha_entity_state_topic = build_ha_state_topic(turned_on_section.id)

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
