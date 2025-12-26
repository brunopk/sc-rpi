"""Contains the `StatusCmd` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.status.status_sc_rpi_result import StatusScRpiResult
from sc_rpi.models.command.command import Command
from sc_rpi.models.command.command_result.status import Status
from sc_rpi.utils.mappings import map_sections

# TODO: return the correct object for each MQTT topic


@dataclass
class StatusCmd(Command[None]):
    """`status` command."""

    name: str = "status"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    def run(self) -> dict[str, DataClassJSONMixin | str]:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        sections = self._hw_controller.list_sections()
        sections = self._hw_controller.list_sections()
        payload = Status(map_sections(sections))

        return StatusScRpiResult(HTTPStatus.ACCEPTED, StatusCmd.name, payload)
