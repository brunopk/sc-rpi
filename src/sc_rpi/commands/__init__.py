"""Contains all available commands (subclasses of `Command`).

All subclasses must be imported before using them in order for mashumaro \
  discriminators to work correctly (see discriminators in \
    [Mashumaro documentation](https://pypi.org/project/mashumaro/)).
"""

from sc_rpi.commands.edit_section.command import EditSection
from sc_rpi.commands.get_config.command import GetConfig
from sc_rpi.commands.help.help_cmd import HelpCmd
from sc_rpi.commands.reset.reset_cmd import ResetCmd
from sc_rpi.commands.status.status_cmd import StatusCmd
from sc_rpi.commands.turn_section_off.turn_section_off_cmd import (
    TurnSectionOffCmd,
)
from sc_rpi.commands.turn_section_on.turn_section_on_cmd import (
    TurnSectionOnCmd,
)
from sc_rpi.commands.version.version_cmd import VersionCmd

__all__ = [
    "EditSectionCmd",
    "GetConfig",
    "HelpCmd",
    "ResetCmd",
    "ResetCmd",
    "StatusCmd",
    "TurnSectionOffCmd",
    "TurnSectionOnCmd",
    "VersionCmd",
]