"""Contains the `SectionRemove` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections


@dataclass
class RemoveSections(Command[list[str]]):
    """`remove_section` command."""

    args: list[str]

    name: str = "remove_section"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """
        if len(self.args) is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Section list is empty",
            )

    def run(self) -> Response:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.remove_sections(self.args)
        self._hw_controller.render()
        sections = self._hw_controller.list_sections()
        result = Status(map_sections(sections))

        return Response(HTTPStatus.ACCEPTED, result)
