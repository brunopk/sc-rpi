"""Contains functions to work with commands."""

from __future__ import annotations

from pathlib import Path


def load_command_paths() -> list[Path]:
    """Load all commands from the commands package (`src.sc_rpi.commands`).

    Returns:
        str[]: Return command paths

    """
    root_package_path = Path(__file__).parent.parent.parent
    commands_package = root_package_path / "models" / "commands" / "all"
    excluded_files = [(commands_package / "__pycache__").name]
    return [
        path
        for path in commands_package.iterdir()
        if (commands_package / path).is_dir() and path.name not in excluded_files
    ]

def load_command_names() -> list[str]:
    """Load all commands from the commands package (`src.sc_rpi.commands`).

    Returns:
        str[]: Return command names

    """
    commands_paths = load_command_paths()
    return [path.stem for path in commands_paths]
