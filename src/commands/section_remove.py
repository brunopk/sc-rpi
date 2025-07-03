"""`section_remove` command."""

from http import HTTPStatus

from jsonschema import Draft7Validator

from command import Command
from controllers import HardwareController
from enums import ErrorCode
from errors import ApiError, ParseError
from models.responses import Response, ResponseOk


class SectionRemove(Command):
    """`section_remove` command."""

    def __init__(self, command_name: str, hw_controller: HardwareController) -> None:
        """Initialize the command.

        Args:
            command_name (str):Extracted from the file name by another module and passed
                in. This is the name shown to users or used to invoke the command.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, hw_controller)
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
        errors = list(self._validator.iter_errors(self.args))
        if len(errors) > 0:
            raise ParseError(errors)
        self._sections: list[str] = self.args["sections"]

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution.
        :raises ApiError: Raises this error when command execution fails for
                          a well-known reason.
        """
        try:
            self._hw_controller.remove_sections(self._sections)
            self._hw_controller.render()
            sections = self._hw_controller.list_sections()
            return ResponseOk(HTTPStatus.ACCEPTED, {"sections": sections})
        except KeyError as ex:
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.SECTION_NOT_FOUND) from ex
