"""Contains functions for command results."""

from http import HTTPStatus

from sc_rpi.commands.results import StatusResult, StatusResultPayload
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.utils.mappings import map_section_list


def build_status_result(
    hw_controller: HardwareController,
    command_name: str,
) -> StatusResult:
    """Build an instance of `StatusResult` representing the result of a command \

    execution.

    Args:
        hw_controller (HardwareController): Used to obtain the current state of SC RPi \
          (which lights are turned on, etc.)
        command_name (str): Name of the command that is being executed

    Returns:
        StatusResult: Instance of `StatusResult` representing the status of SC RPi \
            (sections, active configuration and description)

    """
    sections = hw_controller.list_sections()
    status_result_payload = StatusResultPayload(
        map_section_list(sections),
        hw_controller.get_active_configuration(),
        hw_controller.get_description(),
    )
    return StatusResult(HTTPStatus.ACCEPTED, command_name, status_result_payload)
