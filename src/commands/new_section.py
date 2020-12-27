from command import Command, ParseError
from jsonschema import Draft7Validator


class NewSection(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "start": {
                    "type": "integer",
                },
                "end": {
                    "type": "integer"
                }
            },
            "required": ["from", "to"]
        }
        self.validator = Draft7Validator(arguments_schema)

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)

    def exec(self) -> dict:
        s_id = self.controller.new_section(self.args['from'], self.args['end'])
        return {'id': s_id}

