"""Contains all available commands.

See `Command` class in `src/sc_rpi/commands`.
"""

from sc_rpi.commands import (
    add_section,
    edit_section,
    get_config,
    help,
    remove_sections,
    reset,
    status,
    turn_section_off,
    turn_section_on,
    version,
)

__all__ = [
    "add_section",
    "edit_section",
    "get_config",
    "help",
    "remove_sections",
    "reset",
    "status",
    "turn_section_off",
    "turn_section_on",
    "version",
]
