"""Contains all available commands (subclasses of `Command`).

All subclasses must be imported before using them in order for mashumaro \
  discriminators to work correctly (see discriminators in \
    [Mashumaro documentation](https://pypi.org/project/mashumaro/)).
"""

from sc_rpi.models.commands.all.edit_section.edit_section_cmd import EditSectionCmd
from sc_rpi.models.commands.all.get_config.get_config_cmd import GetConfigCmd
from sc_rpi.models.commands.all.help.help_cmd import HelpCmd
from sc_rpi.models.commands.all.reset.reset_cmd import ResetCmd
from sc_rpi.models.commands.all.status.status_cmd import StatusCmd
from sc_rpi.models.commands.all.turn_section_off.turn_section_off_cmd import (
    TurnSectionOffCmd,
)
from sc_rpi.models.commands.all.turn_section_on.turn_section_on_cmd import (
    TurnSectionOnCmd,
)
from sc_rpi.models.commands.all.version.version_cmd import VersionCmd

__all__ = [
    "EditSectionCmd",
    "GetConfigCmd",
    "HelpCmd",
    "ResetCmd",
    "ResetCmd",
    "StatusCmd",
    "TurnSectionOffCmd",
    "TurnSectionOnCmd",
    "VersionCmd",
]