"""Contains the `TurnSectionOnCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.turn_section_on.turn_section_on_args import TurnSectionOnArgs
from sc_rpi.commands.turn_section_on.turn_section_on_resp import TurnSectionOnResp
from sc_rpi.models.command import Command
from sc_rpi.models.response import Response
from sc_rpi.models.response.status_resp_payload import StatusRespPayload
from sc_rpi.utils.mappings import map_sections


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
        color = (
            (self.args.color.r, self.args.color.g, self.args.color.b)
            if self.args.color is not None
            else None
        )
        self._hw_controller.turn_section_on(self.args.section_id, color)

        self._hw_controller.render()

        sections = self._hw_controller.list_sections()
        payload = StatusRespPayload(map_sections(sections))

        return TurnSectionOnResp(HTTPStatus.ACCEPTED, TurnSectionOnCmd.name, payload)
