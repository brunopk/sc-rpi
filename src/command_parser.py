from importlib import import_module
from json import loads
from os import listdir
from os.path import abspath, dirname, isfile, join

from inflector import Inflector
from jsonschema import Draft7Validator

from command import Command
from controllers import HardwareController
from errors import ParseError


class CommandParser:

    def __init__(self, hw_controller: HardwareController):
        # Dynamically constructs the JSON schema and the Draft7Validator used in the CommandParser
        # IMPORTANT: validate schema with Draft7Validator.check_schema(schema) before using it!

        inflector = Inflector()
        current_path = dirname(abspath(__file__))
        commands_path = join(current_path, 'commands')
        excluded_files = ['__init__.py']
        modules = [
            file_name[:-3]
            for file_name in listdir(commands_path) 
                if isfile(join(commands_path, file_name)) and
                    file_name not in excluded_files
        ]
        schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "enum": modules
                },
                "args": {
                    "type": "object"
                }
            },
            "required": ["name"]
        }
        classes = dict()
        for module_name in modules:
            classes[module_name] = getattr(
                import_module(f'commands.{module_name}'),
                inflector.camelize(module_name))
        self._validator = Draft7Validator(schema)
        self._classes = classes
        self._hw_controller = hw_controller

    def parse(self, json: str) -> Command:
        """
        Parse JSON stringified representation of a command
        :param json: JSON stringified representation of the command
        :return: the corresponding command instance represented in the stringified JSON
        :raises ParseError: in case of parsing an invalid command
        """
        try:
            json = loads(json)
        except Exception:
            raise ParseError(['Invalid JSON'])
        if not isinstance(json, dict):
            raise ParseError(['Invalid JSON'])

        errors = [e.message for e in self._validator.iter_errors(json)]
        if len(errors) > 0:
            raise ParseError(errors)

        # TODO: commands should be initialized in __init__.py

        cmd_name = json['name']
        cmd: Command = self._classes.get(cmd_name)(self._hw_controller)

        if 'args' in json.keys():
            cmd.set_arguments(json['args'])

        return cmd
