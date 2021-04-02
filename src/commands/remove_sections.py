from utils import parse_color
from command import Command
from error import ParseError, ExecutionError
from jsonschema import Draft7Validator


class RemoveSections(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": "strings"
                }
            },
            "required": ["section_id"]
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
            self.controller.remove_sections(self.sections)
            self.controller.render()
        except KeyError:
            raise ExecutionError(f'section {self.args["section_id"]} is not defined')
        except Exception as ex:
            raise ExecutionError(str(ex))

