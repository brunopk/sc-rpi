"""Contains the `ResetCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.models.command.command import Command
from sc_rpi.models.command.command_result.sc_rpi_result import ScRpiResult

# TODO: return the correct object for each MQTT topic


@dataclass
class ResetCmd(Command[None]):
    """`reset` command."""

    name: str = "reset"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> dict[str, DataClassJSONMixin | str]:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.remove_all_sections()
        self._hw_controller.render()

        return ScRpiResult(HTTPStatus.ACCEPTED, ResetCmd.name)
