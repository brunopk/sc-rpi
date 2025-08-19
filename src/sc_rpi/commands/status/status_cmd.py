"""Contains the `StatusCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.status.status_resp import StatusResp
from sc_rpi.models import Response, StatusRespPayload
from sc_rpi.models.command import Command
from sc_rpi.utils import map_sections


@dataclass
class StatusCmd(Command[None]):
    """`status` command."""

    name: str = "status"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._hw_controller.list_sections()
        sections = self._hw_controller.list_sections()
        payload = StatusRespPayload(map_sections(sections))

        return StatusResp(HTTPStatus.ACCEPTED, StatusCmd.name, payload)
