from importlib import import_module
from json import loads
from typing import Optional
from jsonschema import Draft7Validator
from os.path import abspath, isfile, join, dirname
from os import listdir
from inflector import Inflector
from hardware_controller import HardwareController
from errors import ParseError
from response import Response


class Command:
    """

    Commands must be implemented on the *commands* packages following this simple rules:

        - Must me implemented on his own module (inside commands package)
        - Must inherit from this class
        - Class name must be the camelized version of the module name

    Module name will be used as command name.

    """

    def __init__(self):
        self.args: dict = {}
        self.hw_controller: Optional[HardwareController] = None

    def set_hardware_controller(self, controller: HardwareController):
        self.hw_controller = controller

    def set_arguments(self, args: dict):
        """
        Sets the arguments of the command

        :param args: arguments decoded with json.loads
        """
        self.args = args

    def validate_arguments(self):
        """
        :raise ValidationError:
        """
        raise NotImplemented()

    def exec(self) -> Response:
        """
        Executes the command

        :return: result of the execution
        :raises ExecutionError: if command execution fails
        """
        raise NotImplemented()


class CommandParser:

    def __init__(self):
        # Dynamically constructs the JSON schema and the Draft7Validator used in the CommandParser
        # IMPORTANT: validate schema with Draft7Validator.check_schema(schema) before using it!

        inflector = Inflector()
        commands = 'commands'
        current_path = dirname(abspath(__file__))
        excluded_files = ['__init__.py']
        modules = [
            file_name[:-3]
            for file_name in listdir(join(current_path, commands))
            if isfile(join(join(current_path, commands), file_name)) and file_name not in excluded_files
        ]
        schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": modules
                },
                "args": {
                    "type": "object"
                }
            },
            "required": ["command"]
        }
        classes = dict()
        for module_name in modules:
            classes[module_name] = getattr(import_module(f'{commands}.{module_name}'), inflector.camelize(module_name))
        self.validator = Draft7Validator(schema)
        self.classes = classes

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

        errors = [e.message for e in self.validator.iter_errors(json)]
        if len(errors) > 0:
            raise ParseError(errors)

        cmd_name = json['command']
        cmd: Command = self.classes.get(cmd_name)()

        if 'args' in json.keys():
            cmd.set_arguments(json['args'])

        return cmd
