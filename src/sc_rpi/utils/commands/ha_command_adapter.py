"""Contains the map_to_sc_rpi_command function."""

from sc_rpi.commands.turn_section_off import TurnSectionOffCmd
from sc_rpi.commands.turn_section_on import TurnSectionOnCmd
from sc_rpi.models.command import Command
from sc_rpi.models.homeassistant import HACommand

# TODO: move this to main.py (rename command_utils.py to main.py)

def map_ha_command_to_sc_rpi_command(ha_command: HACommand) -> Command:
  """Map a command from Home Assistant to the equivalent SC RPi command.

  Args:
      ha_command (HACommand): Command to be mapped

  Returns:
      Command: Return the equivalent SC RPi command.

  Raises:
      ApiError:

  """
  if ha_command.color is None:
    # TODO: CONTINUE (use the State enum into HACommand)
    return Command()