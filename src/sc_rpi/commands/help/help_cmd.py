"""Contains the `HelpCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.help.help_resp import HelpResp
from sc_rpi.commands.help.help_resp_payload import HelpRespPayload
from sc_rpi.models.command import Command
from sc_rpi.utils.commands.dynamic_loading import load_command_names


@dataclass
class HelpCmd(Command[None]):
    """`help` command."""

    name: str = "help"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> HelpResp:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        command_names = load_command_names()
        payload = HelpRespPayload(sorted(command_names))

        return HelpResp(HTTPStatus.ACCEPTED, HelpCmd.name, payload)
