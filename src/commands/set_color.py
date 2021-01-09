from utils import parse_color
from command import Command, ParseError, ExecutionError
from jsonschema import Draft7Validator


class SetColor(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "section": {
                    "type": "integer",
                },
                "color": {
                    "typeof": "string"
                }
            },
            "required": ["color"]
        }
        self.validator = Draft7Validator(arguments_schema)
        self.color = None
        self.section = None

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)
        try:
            self.color = parse_color(self.args["color"])
        except ValueError:
            errors = ['color must be an hex or in rgb format']
            raise ParseError(errors)

    def exec(self):
        try:
            if 'section' in self.args.keys():
                self.controller.set_color(self.args['section'], self.color)
            else:
                self.controller.set_color(self.color)
            self.controller.render_strip()
        except KeyError:
            raise ExecutionError(f'section {self.args["section"]} is not defined')
