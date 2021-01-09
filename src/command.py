from importlib import import_module
from json import loads
from typing import List, Union, Optional
from jsonschema import Draft7Validator, ValidationError
from os.path import abspath, isfile, join, dirname
from os import listdir
from inflector import Inflector
from controller import Controller


def get_path(e: ValidationError) -> str:
    return f'arguments.{".".join([e for e in e.absolute_path])}'


class ParseError(Exception):

    def __init__(self, errors: List[Union[ValidationError, str]]):
        aux1 = [f'error in {get_path(e)} : {e.message}' for e in errors if isinstance(e, ValidationError)]
        aux2 = [e for e in errors if isinstance(e, str)]
        self.errors = aux1 if len(aux1) > 0 else aux2


class ExecutionError(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def get_msg(self):
        return self.msg


class Command:
    """

    Commands must be implemented on the *commands* packages following this simple rules:

        - Must me implemented on his own module (inside commands package)
        - Must inherit from this class
        - Class name must be the camelized version of the module name

    The command name (the value for the *name* attribute on the JSON) will be the same
    as the module name (snake-case version).

    """

    def __init__(self):
        self.args: dict = None
        self.controller: Optional[Controller] = None

    def set_controller(self, controller: Controller):
        self.controller = controller

    def set_arguments(self, args: dict):
        """
        Sets the arguments of the command

        :param args: arguments decoded with json.loads
        """
        self.args = args

    def validate_arguments(self):
        """
        Raises ParseError exception if command don't pass validations
        """
        raise NotImplemented()

    def exec(self) -> dict:
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
            for file_name in listdir(commands)
            if isfile(join(join(current_path, commands), file_name)) and file_name not in excluded_files
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
            classes[module_name] = getattr(import_module(f'{commands}.{module_name}'), inflector.camelize(module_name))
        self.validator = Draft7Validator(schema)
        self.classes = classes

    def parse(self, json: str) -> Command:
        """
        Parse and validates a JSON stringified representation of a command
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
        cmd: Command = self.classes.get(cmd_name)()

        if 'args' in json.keys():
            cmd.set_arguments(json['args'])
            cmd.validate_arguments()

        return cmd
