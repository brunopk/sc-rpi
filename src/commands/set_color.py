import re
from command import Command, ParseError, ExecutionError
from jsonschema import Draft7Validator
from webcolors import hex_to_rgb
from rpi_ws218x import Color


def parse_color(c: str) -> Color:
    try:
        c = hex_to_rgb(c)
        (red, blue, green) = c.red, c.green, c.blue
    except ValueError as e:
        regex_rgb = r"^rgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$"
        match = re.match(regex_rgb, c)
        if match is not None:
            red = int(match.groups()[0])
            green = int(match.groups()[1])
            blue = int(match.groups()[2])
            if 0 > red or 0 > green or 0 > blue or 255 < red or 255 < green or 255 < blue:
                raise ValueError()
        else:
            raise ValueError()
    return Color(red, green, blue)


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
                array = self.controller.get_section_by_id(self.args['section'])
                array = [self.color] * len(array)
                self.controller.update_section(self.args['section'], array)
            else:
                self.controller.set_color(self.color)
            self.controller.render_strip()
        except KeyError:
            raise ExecutionError(f'section {self.args["section"]} is not defined')
