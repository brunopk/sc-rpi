"""Contains the `HelpCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.help.result import HelpResult, HelpResultPayload
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.dynamic_loading import load_command_names
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC


@dataclass
class Help(Command[None]):
    """`help` command."""

    command_name: str = "help"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        command_names = load_command_names()
        payload = HelpResultPayload(sorted(command_names))
        result = HelpResult(
            HTTPStatus.ACCEPTED,
            HelpCmd.command_name,
            payload,
        )

        return {SC_RPI_RESULT_TOPIC: result }
