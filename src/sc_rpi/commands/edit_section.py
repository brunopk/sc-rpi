"""Contains the `SectionEdit` class."""
from __future__ import annotations

from http import HTTPStatus
from typing import Any

from jsonschema import Draft7Validator
from webcolors import hex_to_rgb

from sc_rpi.utils.commands.command import Command
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError, ParseError
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections


class EditSection(Command):
    """`edit_section` command."""

    _DRAFT_VALIDATOR = Draft7Validator({
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
    })

    def __init__(self, command_arguments: dict | None, **kwargs: Any) -> None:
        """Initialize the instance (constructor).

        Args:
            command_arguments (dict | None): Command arguments (defined by user).
            kwargs (Any): Arguments as defined in `Command` (`config`, \
                `hw_controller`, etc).

        """
        super().__init__(command_arguments, **kwargs)

    def run(self) -> Response:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        if self._command_args is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "args not defined",
            )
        if "color" in self._command_args:
            try:
                color = hex_to_rgb(self._command_args["color"])
            except ValueError as ex:
                errors = ["color must be in hex format"]
                raise ParseError(errors) from ex
            else:
                color = None
        else:
            color = None
        start = self._command_args.get("start", None)
        end = self._command_args.get("end", None)
        section_id = self._command_args.get("section_id", None)
        if section_id is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.SECTION_NOT_FOUND,
                f"section {self._command_args['section_id']} is not defined",
            )

        self._hw_controller.edit_section(section_id, start, end, color)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        result = Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
