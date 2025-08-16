"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.turn_section_on.turn_section_on_args import TurnSectionOnArgs
from sc_rpi.models import Response, StatusResp
from sc_rpi.models.command import Command
from sc_rpi.utils import map_sections


@dataclass
class TurnSectionOnCmd(Command[TurnSectionOnArgs]):
    """`turn_section_on` command."""

    args: TurnSectionOnArgs

    name: str = "turn_section_on"

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        self._hw_controller.turn_on(self.args.section_id)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        resp = StatusResp(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, TurnSectionOnCmd.name, resp)
