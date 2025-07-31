"""Contains the `Status` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.models import responses
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response
from sc_rpi.utils import map_sections


@dataclass
class Status(Command[None]):
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
        result = responses.commands.Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
