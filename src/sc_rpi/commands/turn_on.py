"""Contains the `TurnOn` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from jsonschema import Draft7Validator

from sc_rpi.utils.commands.command import Command
from sc_rpi.errors import ParseError
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections


class TurnOn(Command):
    """`turn_on` command."""

    _DRAFT_VALIDATOR = Draft7Validator({
        "$schema": "https://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "section_id": {
                "type": "string",
            },
        },
    })

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

        Raises:
            ApiError:
            ParseError:

        """
        validator = self._DRAFT_VALIDATOR
        if self._command_args is not None:
            errors = [
                e.message for e in validator.iter_errors(self._command_args)
            ]
            if len(errors) > 0:
                raise ParseError(errors)

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        section_id = (
            None
            if self._command_args is None
            else self._command_args.get("section_id", None)
        )
        self._hw_controller.turn_on(section_id)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        result = Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
