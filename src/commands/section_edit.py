"""`section_edit` command."""
from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from jsonschema import Draft7Validator

from command import Command
from enums import ErrorCode
from errors import ApiError, ParseError
from helpers import parse_color
from models import Response, ResponseOk

if TYPE_CHECKING:
    from controllers import HardwareController

class SectionEdit(Command):
    """`section_edit` command."""

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            command_name (str):Extracted from the file name by another module and
                passed in. This is the name shown to users or used to invoke the 
                command.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, hw_controller)
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "section_id": {
                    "type": "string",
                },
                "start": {
                    "type": "integer",
                },
                "end": {
                    "type": "integer",
                },
                "color": {
                    "type": "string",
                    "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
                }
            },
            "required": ["section_id"],
        }
        self._validator = Draft7Validator(arguments_schema)

    def validate_arguments(self) -> None:
        """Validate command arguments."""
        errors = list(self._validator.iter_errors(self._args))
        if len(errors) > 0:
            raise ParseError(errors)
        if "color" in self._args:
            try:
                self._color = parse_color(self._args["color"])
            except ValueError as ex:
                errors = ["color must be an hex or in rgb format"]
                raise ParseError(errors) from ex
        self._start = self._args.get("start", None)
        self._end = self._args.get("end", None)
        self._section_id: str = self._args["section_id"]

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution.
        :raises ApiError: Raises this error when command execution fails for
                          a well-known reason.
        """
        try:
            self._hw_controller.edit_section(
                self._section_id, self._start, self._end, self._color
            )
            self._hw_controller.render()
            return ResponseOk(HTTPStatus.OK, self._command_name)
        except KeyError as ex:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.SECTION_NOT_FOUND,
                f"section {self._args['section_id']} is not defined",
            ) from ex
