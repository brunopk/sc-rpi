"""Contains functions to work commands."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import TYPE_CHECKING

from inflector import Inflector

from sc_rpi.errors import ApiError

if TYPE_CHECKING:
    from sc_rpi.command import Command



def load_command_paths() -> list[Path]:
    """Load all commands from the commands package (`src.commands`).

    Returns:
        str[]: Return command paths

    """
    root_path = Path(__file__).parent.parent.parent
    commands_package = root_path / "commands"
    excluded_files = [(commands_package / "__init__.py").name]
    return [
        path
        for path in commands_package.iterdir()
        if (commands_package / path).is_file() and path.name not in excluded_files
    ]

def load_command_names() -> list[str]:
    """Load all commands from the commands package (`src.commands`).

    Returns:
        str[]: Return command names

    """
    commands_paths = load_command_paths()
    return [path.stem for path in commands_paths]

def load_commands() -> dict[str, type[Command]]:
    """Load all commands (instances) from the commands package (src.commands).

    Returns:
        dict[str, type[Command]]: Return a dictionary whose keys are the command names \
          (snake-case)

    """
    command_dictionary: dict[str, type[Command]] = {}
    command_paths = load_command_paths()
    command_names = load_command_names()
    inflector = Inflector()

    for index, command_name in enumerate(command_names):
        module_spec = spec_from_file_location(
            command_name,
            str(command_paths[index]),
        )
        if module_spec is None:
            raise ApiError(
                message=f"ModuleSpec for {command_paths[index].name} is None",
            )
        if module_spec.loader is None:
            raise ApiError(
                message=f"ModuleSpec.loader for {command_paths[index].name}is None",
            )
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        command_dictionary[command_name] = getattr(
            module,
            inflector.camelize(command_name),
        )

    return command_dictionary
