"""Contains the `HelpCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.help.help_sc_rpi_result import HelpScRpiResult
from sc_rpi.commands.help.help_sc_rpi_result_payload import HelpScRpiResultPayload
from sc_rpi.models.command.command import Command, CommandResult
from sc_rpi.utils.commands.decorators import log_call
from sc_rpi.utils.commands.dynamic_loading import load_command_names
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC


@dataclass
class HelpCmd(Command[None]):
    """`help` command."""

    name: str = "help"

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
        command_names = load_command_names()
        payload = HelpScRpiResultPayload(sorted(command_names))
        sc_rpi_result = HelpScRpiResult(HTTPStatus.ACCEPTED, HelpCmd.name, payload)
        return {SC_RPI_RESULT_TOPIC: sc_rpi_result }
