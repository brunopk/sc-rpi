"""Contains the `Help` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.models import responses
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response
from sc_rpi.utils.commands import command_utils


@dataclass
class Help(Command[None]):
    """`help` command."""

    name: str = "help"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        command_names = command_utils.load_command_names()
        result = responses.commands.Help(sorted(command_names))

        return Response(HTTPStatus.ACCEPTED, result)
