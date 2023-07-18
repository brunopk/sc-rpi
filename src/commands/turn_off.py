from utils import parse_color
from jsonschema import Draft7Validator
from command import Command
from errors import ParseError, ApiError
from enums import ErrorCode


class TurnOff(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "section_id": {
                    "type": "string",
                }
            },
        }
        self.validator = Draft7Validator(arguments_schema)

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)

    def exec(self):
        section_id = self.args['section_id'] if 'section_id' in self.args else None
        try:
            self.controller.turn_off(section_id)
        except KeyError as e:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)
