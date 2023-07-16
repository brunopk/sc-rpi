from utils import parse_color
from command import Command
from errors import ParseError, ApiError
from jsonschema import Draft7Validator


# TODO: SEGUIR REVISANDO SI ESTA TODO BIEN DESPUES DE LOS CAMBIOS DE MANEJO DE ERRORES


class SectionEdit(Command):

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
                    "type": "string",
                    "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"
                }
            },
            "required": ["section_id"]
        }
        self.section_id = None
        self.color = None
        self.start = None
        self.end = None
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
        self.start = self.args['start'] if 'start' in self.args.keys() else None
        self.end = self.args['end'] if 'end' in self.args.keys() else None
        self.section_id = self.args['section_id']

    def exec(self):
        try:
            self.controller.edit_section(self.section_id, self.start, self.end, self.color)
            self.controller.render()
        except KeyError:
            raise ExecutionError(f'section {self.args["section_id"]} is not defined')
        except ValueError as ex:
            raise ExecutionError(str(ex))

