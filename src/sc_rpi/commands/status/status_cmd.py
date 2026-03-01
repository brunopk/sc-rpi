"""Contains the `StatusCmd` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.commands.results import build_sc_rpi_status_result
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC

# TODO: CONTINUE do the same refact that was done for reset

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
        sc_rpi_result = build_sc_rpi_status_result(
            self._hw_controller,
            self.command_name,
        )

        return {SC_RPI_RESULT_TOPIC: sc_rpi_result}
