"""Contains the `ResetCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response


@dataclass
class ResetCmd(Command[None]):
    """`reset` command."""

    name: str = "reset"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> Response:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()

        return Response(HTTPStatus.ACCEPTED, ResetCmd.name)
