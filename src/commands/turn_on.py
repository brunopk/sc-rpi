"""`turn_on` command."""

from http import HTTPStatus

from jsonschema import Draft7Validator

from command import Command
from controllers import HardwareController
from enums import ErrorCode
from errors import ApiError, ParseError
from models import Response, ResponseOk


class TurnOn(Command):
    """`turn_on` command."""

    CMD_NAME = "turn_on"

    def __init__(self, hw_controller: HardwareController) -> None:
        """`turn_on` command."""
        super().__init__(hw_controller)
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "section_id": {
                    "type": "string",
                },
            },
        }
        self._validator = Draft7Validator(arguments_schema)

    def validate_arguments(self) -> None:
        """Validate command arguments."""
        if self._args is None:
            return

        errors = list(self._validator.iter_errors(self._args))
        if len(errors) > 0:
            raise ParseError(errors)

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution.
        :raises ApiError: Raises this error when command execution fails for
                          a well-known reason.
        """
        try:
            section_id = (
                self._args["section_id"]
                if self._args is not None and "section_id" in self._args
                else None
            )
            self._hw_controller.turn_on(section_id)
            self._hw_controller.render()
            return ResponseOk(HTTPStatus.ACCEPTED, TurnOn.CMD_NAME)
        except KeyError as ex:
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.SECTION_NOT_FOUND) from ex
