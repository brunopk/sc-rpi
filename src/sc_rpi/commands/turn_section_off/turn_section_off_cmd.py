"""Contains the `TurnSectionOffCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.turn_section_off.turn_section_off_args import TurnSectionOffArgs
from sc_rpi.commands.turn_section_off.turn_section_off_sc_rpi_result import (
    TurnSectionScRpiResult,
)
from sc_rpi.models.command.command import Command
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.utils.mappings import map_sections

if TYPE_CHECKING:
    from mashumaro.mixins.json import DataClassJSONMixin

# TODO: return the correct object for each MQTT topic

# TODO: CONTINUE

@dataclass
class TurnSectionOffCmd(Command[TurnSectionOffArgs]):
    """`turn_section_off` command."""

    args: TurnSectionOffArgs

    name: str = "turn_section_off"

    def run(self) -> dict[str, DataClassJSONMixin | str]:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_off(self.args.section_id)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        payload = Status(map_sections(sections))

        # TODO: CONTINUE send the correct message for each topic

        return TurnSectionScRpiResult(HTTPStatus.ACCEPTED, TurnSectionOffCmd.name, payload)
