"""Contains the `ResetCmd` class."""

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.results.sc_rpi_status_result import ScRpiStatusResult
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.commands.results import build_sc_rpi_status_result
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC


@dataclass
class ResetCmd(Command[ScRpiStatusResult]):
    """`reset` command."""

    command_name: str = "reset"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_call()
    def run(self) -> CommandResult:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()
        sc_rpi_result = build_sc_rpi_status_result(
            self._hw_controller,
            self.command_name,
        )

        return { SC_RPI_RESULT_TOPIC: sc_rpi_result }
