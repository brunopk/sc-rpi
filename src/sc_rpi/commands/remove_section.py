"""Contains the `SectionRemove` class."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from jsonschema import Draft7Validator

from sc_rpi.utils.commands.command import Command
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections


class RemoveSection(Command):
    """`remove_section` command."""

    _DRAFT_VALIDATOR = Draft7Validator({
        "$schema": "https://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "sections": {
                "type": "array",
                "items": {
                    "type": "string",
                },
            },
        },
        "required": ["sections"],
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
        sections_to_remove: list[str] | None = self._command_args.get("sections")
        if sections_to_remove is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.SECTION_NOT_FOUND,
                "sections not defined",
            )

        self._hw_controller.remove_sections(sections_to_remove)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        result = Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
