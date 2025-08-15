"""Contains the `TurnSectionOffCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.turn_section_off.turn_section_off_args import TurnSectionOffArgs
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections


@dataclass
class TurnSectionOffCmd(Command[TurnSectionOffArgs]):
    """`turn_section_off` command."""

    args: TurnSectionOffArgs

    name: str = "turn_section_off"

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_off(self.args.section_id)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        result = Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
