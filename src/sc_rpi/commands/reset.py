"""Contains the `Reset` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from sc_rpi.utils.commands.command import Command
from sc_rpi.models.responses import Response


class Reset(Command):
    """`reset` command."""

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

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()

        return Response(HTTPStatus.ACCEPTED)
