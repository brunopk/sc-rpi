"""Contains the `Status` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from sc_rpi.utils.commands.command import Command
from sc_rpi.models import responses
from sc_rpi.models.responses import Response
from sc_rpi.utils import map_sections


class Status(Command):
    """`status` command."""

    def __init__(self, command_arguments: dict | None, **kwargs: Any) -> None:
        """Initialize the instance (constructor).

        Args:
            command_arguments (dict | None): Command arguments (defined by user).
            kwargs (Any): Arguments as defined in `Command` (`config`, \
                `hw_controller`, etc).

        """
        super().__init__(command_arguments, **kwargs)

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
