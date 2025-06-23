"""`section_remove` command."""

from http import HTTPStatus

from jsonschema import Draft7Validator

from command import Command
from controllers import HardwareController
from enums import ErrorCode
from errors import ApiError, ParseError
from models import Response, ResponseOk


class SectionRemove(Command):
    """`section_remove` command."""

    CMD_NAME = "section_remove"

    def __init__(self, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(hw_controller)
        arguments_schema = {
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
        }
        self._validator = Draft7Validator(arguments_schema)

    def validate_arguments(self) -> None:
        """Validate command arguments."""
        errors = list(self._validator.iter_errors(self._args))
        if len(errors) > 0:
            raise ParseError(errors)
        self._sections: list[str] = self._args["sections"]

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution.
        :raises ApiError: Raises this error when command execution fails for
                          a well-known reason.
        """
        try:
            self._hw_controller.remove_sections(self._sections)
            self._hw_controller.render()
            return ResponseOk(HTTPStatus.ACCEPTED, SectionRemove.CMD_NAME)
        except KeyError as ex:
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.SECTION_NOT_FOUND) from ex
