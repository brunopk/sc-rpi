"""Contains `apply_named_config`, shared by `use_config` and `reset`."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from sc_rpi.commands.results import StatusResult, StatusResultPayload
from sc_rpi.utils.config import store
from sc_rpi.utils.homeassistant import build_ha_refresh_messages
from sc_rpi.utils.mappings import map_section_list
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC

if TYPE_CHECKING:
    from sc_rpi.commands.base import CommandResult
    from sc_rpi.controllers.hardware_controller import HardwareController


def apply_named_config(
    hw_controller: HardwareController,
    command_name: str,
    config_name: str | None,
    brightness: int,
) -> CommandResult:
    """Apply the saved config `config_name` all-or-nothing and build the result.

    Nothing that can fail runs once the strip has changed.

    Args:
        hw_controller (HardwareController): Strip to modify.
        command_name (str): Name of the command, used in the SC RPi result.
        config_name (str | None): Name of the saved config to apply.
        brightness (int): Default section brightness sent in the Home Assistant states.

    Raises:
        ApiError: `MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME`, `CONFIG_NOT_FOUND` or
            `INVALID_CONFIG`; the strip and the sections are unchanged.

    Returns:
        CommandResult: Topic -> payload, in the order to publish.

    """
    name = store.validate_name(config_name)
    loaded = store.load(name)
    previous_sections = hw_controller.list_sections()
    prepared = hw_controller.prepare_config(loaded)

    result: CommandResult = {
        SC_RPI_RESULT_TOPIC: StatusResult(
            HTTPStatus.ACCEPTED,
            command_name,
            StatusResultPayload(map_section_list(prepared)),
        ),
    }
    result.update(build_ha_refresh_messages(previous_sections, prepared, brightness))

    hw_controller.apply_prepared(prepared, loaded.description)
    return result
