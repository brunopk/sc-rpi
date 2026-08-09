"""Contains all available commands (subclasses of `Command`).

All subclasses must be imported before using them in order for mashumaro \
  discriminators to work correctly (see discriminators in \
    [Mashumaro documentation](https://pypi.org/project/mashumaro/)).
"""

from sc_rpi.commands.base import Command
from sc_rpi.commands.edit_section.command import EditSection
from sc_rpi.commands.get_config.command import GetConfig
from sc_rpi.commands.help.command import Help
from sc_rpi.commands.reset.command import Reset
from sc_rpi.commands.status.command import StatusCmd
from sc_rpi.commands.turn_section_off.command import TurnSectionOffCmd
from sc_rpi.commands.turn_section_on.command import TurnSectionOnCmd
from sc_rpi.commands.version.command import VersionCmd

__all__ = [
    "Command",
    "EditSection",
    "GetConfig",
    "Help",
    "Reset",
    "StatusCmd",
    "TurnSectionOffCmd",
    "TurnSectionOnCmd",
    "VersionCmd",
]
