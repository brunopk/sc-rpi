"""Contains the `StatusCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.models.commands.all.status.status_sc_rpi_result import StatusScRpiResult
from sc_rpi.models.commands.command import Command, CommandResult
from sc_rpi.models.commands.command_result.status import Status
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.mappings import map_sections
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC


@dataclass
class StatusCmd(Command[None]):
    """`status` command."""

    command_name: str = "status"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._hw_controller.list_sections()
        sections = self._hw_controller.list_sections()
        payload = Status(map_sections(sections))
        sc_rpi_result = StatusScRpiResult(
            HTTPStatus.ACCEPTED,
            StatusCmd.command_name,
            payload,
        )

        return {SC_RPI_RESULT_TOPIC: sc_rpi_result}
