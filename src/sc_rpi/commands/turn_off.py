"""Contains the `TurnOff` class."""

from http import HTTPStatus

from jsonschema import Draft7Validator

from sc_rpi.command import Command
from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError, ParseError
from sc_rpi.models.responses import Response, ResponseOk
from sc_rpi.utils import Collector


class TurnOff(Command):
    """`turn_off` command."""

    def __init__(
        self,
        command_name: str,
        config: Config,
        hw_controller: HardwareController,
        collector: Collector,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.
            collector (Collector): Used to collect information of clients of SC RPI.

        """
        super().__init__(command_name, config, hw_controller, collector)
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
        errors = list(self._validator.iter_errors(self.args))
        if len(errors) > 0:
            raise ParseError(errors)

    def run(self) -> Response:
        """Execute the command.

        :return Response: Returns this object with result of the execution.
        """
        section_id = self.args.get("section_id", None)
        try:
            self._hw_controller.turn_off(section_id)
            self._hw_controller.render()
            sections = self._hw_controller.list_sections()
            return ResponseOk(HTTPStatus.ACCEPTED, {"sections": sections})
        except KeyError as ex:
            raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.SECTION_NOT_FOUND) from ex
