from utils import parse_color
from jsonschema import Draft7Validator
from command import Command
from errors import ParseError, ApiError
from enums import ErrorCode


class SectionRemove(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["sections"]
        }
        self.sections = None
        self.validator = Draft7Validator(arguments_schema)

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)
        self.sections = self.args['sections']

    def exec(self):
        try:
            self.hw_controller.remove_sections(self.sections)
            self.hw_controller.render()
        except KeyError as ex:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)
