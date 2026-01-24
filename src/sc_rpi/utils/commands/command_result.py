"""Contains functions for command results."""

from http import HTTPStatus

from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.models.commands.command_result.sc_rpi_status_result import ScRpiStatusResult
from sc_rpi.models.commands.command_result.status import Status
from sc_rpi.utils.mappings import map_sections


def build_sc_rpi_status_result(
    hw_controller: HardwareController,
    command_name: str,
) -> ScRpiStatusResult:
    """Build an instance of `ScRpiStatusResult` representing the result of a command \

    execution.
    `ScRpiStatusResult` is used for commands that should return the same result.

    Args:
        hw_controller (HardwareController): Used to obtain the current state of SC RPi \
          (which lights are turned on, etc.)
        command_name (str): Name of the command that is being executed

    Returns:
        ScRpiStatusResult: Instance of `ScRpiStatusResult` representing the result of \
          executing a command (`command_name`)

    """
    sections = hw_controller.list_sections()
    sc_rpi_result_payload = Status(map_sections(sections))
    return ScRpiStatusResult(
        HTTPStatus.ACCEPTED,
        command_name,
        sc_rpi_result_payload,
    )
