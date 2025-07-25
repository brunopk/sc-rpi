"""Contains functions to work commands."""

from __future__ import annotations

from pathlib import Path


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
