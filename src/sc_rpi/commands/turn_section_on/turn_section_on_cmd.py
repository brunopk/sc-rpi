"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from webcolors import hex_to_rgb

from sc_rpi.commands.turn_section_on.turn_section_on_args import TurnSectionOnArgs
from sc_rpi.commands.turn_section_on.turn_section_on_resp import TurnSectionOnResp
from sc_rpi.models import Response, StatusRespPayload
from sc_rpi.models.command import Command

# TODO: use rgb notation in all places instead of hex

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
        # TODO: CONTINUE
        self._hw_controller.turn_on(self.args.section_id)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        payload = StatusRespPayload(map_sections(sections))

        return TurnSectionOnResp(HTTPStatus.ACCEPTED, TurnSectionOnCmd.name, payload)
