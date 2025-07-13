"""Contains the `Help` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from sc_rpi.command import Command
from sc_rpi.models import responses
from sc_rpi.models.responses import Response
from sc_rpi.utils.commands import command_utils


class Help(Command):
    """`help` command."""

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
        command_names = command_utils.load_command_names()
        result = responses.commands.Help(sorted(command_names))

        return Response(HTTPStatus.ACCEPTED, result)
