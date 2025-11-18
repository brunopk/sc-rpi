"""Contains functions to map between different command objects."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.turn_section_off import TurnSectionOffCmd
from sc_rpi.commands.turn_section_off.turn_section_off_args import TurnSectionOffArgs
from sc_rpi.commands.turn_section_on import TurnSectionOnCmd
from sc_rpi.commands.turn_section_on.turn_section_on_args import TurnSectionOnArgs
from sc_rpi.enums import ErrorCode
from sc_rpi.enums.homeassistant import State
from sc_rpi.errors import ApiError
from sc_rpi.utils.mqtt import get_object_id_from_ha_command_topic

if TYPE_CHECKING:
    from sc_rpi.controllers.hardware_controller import HardwareController
    from sc_rpi.models.command import Command
    from sc_rpi.models.config.config import Config
    from sc_rpi.models.homeassistant import HACommand

def map_ha_command_to_sc_rpi_command(
    ha_command: HACommand,
    ha_command_topic: str,
    sc_rpi_config: Config,
    hw_controller: HardwareController,
) -> Command | None:
    """Map a command from Home Assistant to the equivalent SC RPi command.

    Args:
        ha_command (HACommand): Command to be mapped
        ha_command_topic (str): Used to identify the section (entity) of the strip to \
            which command was sent.
        sc_rpi_config (Config): Used to build the SC RPi command.
        hw_controller (HardwareController): Used to build the SC RPi command.

    Returns:
        Command: Return the equivalent SC RPi command.

    Raises:
        ApiError:

    """
    section_id = get_object_id_from_ha_command_topic(ha_command_topic)

    if ha_command.state == State.ON:
        cmd_args = TurnSectionOnArgs(section_id)
        return TurnSectionOnCmd(
            args=cmd_args,
            _config=sc_rpi_config,
            _hw_controller=hw_controller,
        )
    if ha_command.state == State.OFF:
        cmd_args = TurnSectionOffArgs(section_id)
        return TurnSectionOffCmd(
            args=cmd_args,
            _config=sc_rpi_config,
            _hw_controller=hw_controller,
        )

    raise ApiError(
        HTTPStatus.BAD_REQUEST,
        ErrorCode.INVALID_COMMAND,
        "Cannot map Home Assistant command to SC RPi command",
    )
