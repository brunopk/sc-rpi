from utils import parse_color
from command import Command, ParseError, ExecutionError
from jsonschema import Draft7Validator


class EditSection(Command):

    def __init__(self):
        super().__init__()
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "section_id": {
                    "type": "string"
                },
                "start": {
                    "type": "integer"
                },
                "end": {
                    "type": "integer"
                },
                "color": {
                    "type": "string"
                }
            },
            "required": ["section_id"]
        }
        self.color = None
        self.validator = Draft7Validator(arguments_schema)

    def validate_arguments(self):
        errors = [e for e in self.validator.iter_errors(self.args)]
        if len(errors) > 0:
            raise ParseError(errors)
        if 'color' in self.args.keys():
            try:
                self.color = parse_color(self.args['color'])
            except ValueError:
                errors = ['color must be an hex or in rgb format']
                raise ParseError(errors)

    def exec(self):
        section_id = self.args['section_id']
        start = self.args['start'] if 'start' in self.args.keys() else None
        end = self.args['end'] if 'end' in self.args.keys() else None
        try:
            section = self.controller.get_section(section_id)
            start = start if start is not None else section.get_indexes()[0]
            end = end if end is not None else section.get_indexes()[1]
            color_list = [self.color] * (end - start + 1) if self.color is not None else section.get_color_list()
            self.controller.edit_section(section_id, start, end, color_list)
        except KeyError:
            raise ExecutionError(f'section {self.args["section_id"]} is not defined')
        except ValueError as ex:
            raise ExecutionError(str(ex))

