from importlib import import_module
from json import loads
from typing import Optional
from os import listdir
from os.path import abspath, isfile, join, dirname
from jsonschema import Draft7Validator
from inflector import Inflector
from errors import ParseError
from response import Response
from controller import Controller

class Command:
    """
    To implement a command:

    - It must be implemented in its own module within the commands package.
    - The command class must inherit from this class and be named using the camelized version of the 
    module name. For example, if the module is section_add.py, the class name should be SectionAdd.
    
    The command name for JSON representation will be generated from the module name.
    
    """

    def __init__(self, controller: Controller):
        self.args: dict = {}
        self.controller = controller

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
        raise NotImplementedError()

    def exec(self) -> Response:
        """
        Executes the command

        :return: result of the execution
        :raises ExecutionError: if command execution fails
        """
        raise NotImplementedError()


class CommandParser:

    def __init__(self, controller: Controller):
        # Dynamically constructs the JSON schema and the Draft7Validator used in the CommandParser
        # IMPORTANT: validate schema with Draft7Validator.check_schema(schema) before using it!

        inflector = Inflector()
        current_path = dirname(abspath(__file__))
        excluded_files = ['__init__.py']
        modules = [
            file_name[:-3]
            for file_name in listdir(current_path) 
                if isfile(join(current_path, file_name)) and
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
        self.validator = Draft7Validator(schema)
        self.classes = classes
        self.controller = controller

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

        cmd_name = json['name']
        cmd: Command = self.classes.get(cmd_name)(self.controller)

        if 'args' in json.keys():
            cmd.set_arguments(json['args'])

        return cmd
