"""Contains the `CommandParser` class."""
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from json import loads
from typing import TYPE_CHECKING

from inflector import Inflector
from jsonschema import Draft7Validator

from errors import ApiError, ParseError

from .commands import load_command_names, load_command_paths
from utils import Collector

if TYPE_CHECKING:
    from command import Command
    from controllers import HardwareController

class CommandParser:
    """Used to parse commands (stringified JSON objects).

    Important: before using a schema (draft schema) validate it with
    `Draft7Validator.check_schema(schema)` before using that schema.
    """

    def __init__(self, hw_controller: HardwareController, collector: Collector) -> None:
        """Initialize the command parser.

        Args:
            hw_controller (HardwareController): Used to control the strip.
            collector (Collector): Used to collect information of clients of SC RPI.

        """
        command_paths = load_command_paths()
        command_names = load_command_names()
        schema = {
            "$schema": "https://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "enum": command_names,
                },
                "args": {
                    "type": "object",
                },
            },
            "required": ["name"],
        }
        self._validator = Draft7Validator(schema)

        commands: dict[str, type[Command]] = {}
        inflector = Inflector()
        for index, command_name in enumerate(command_names):
            module_spec = spec_from_file_location(
                command_name, str(command_paths[index]),
            )
            if module_spec is None:
                raise ApiError(
                    message=f"ModuleSpec for {commands_paths[index].name} is None",
                )
            if module_spec.loader is None:
                raise ApiError(
                    message=f"ModuleSpec.loader for {commands_paths[index].name} is None",
                )
            module = module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            commands[command_name] = getattr(module, inflector.camelize(command_name))
        self._commands = commands

        self._hw_controller = hw_controller
        self._collector = collector

    def parse(self, json: str) -> Command:
        """Parse JSON stringified representation of a command.

        Args:
            json (str): stringified command.

        Raises:
            ParseError:
            ApiError:

        Returns:
            Command: Returns the corresponding command instance.

        """
        try:
            cmd_as_dict: dict = loads(json)
        except Exception as ex:
            raise ParseError(["Invalid JSON"]) from ex
        if not isinstance(cmd_as_dict, dict):
            raise ParseError(["Invalid JSON"])

        # Validates syntax errors
        errors = [e.message for e in self._validator.iter_errors(cmd_as_dict)]
        if len(errors) > 0:
            raise ParseError(errors)

        # Obtain the command instance
        cmd_name = cmd_as_dict["name"]
        cmd_class = self._commands.get(cmd_name)
        if cmd_class is None:
            raise ApiError
        cmd_instance = cmd_class(cmd_name, self._hw_controller, self._collector)
        if "args" in json:
            cmd_instance.args = cmd_as_dict["args"]

        return cmd_instance
