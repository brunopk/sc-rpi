"""Contains the `SectionAdd` class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING

from jsonschema import Draft7Validator
from webcolors import hex_to_rgb

from sc_rpi.command import Command
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError, ParseError
from sc_rpi.models.responses import Response, ResponseOk
from sc_rpi.utils import map_sections

if TYPE_CHECKING:
    from sc_rpi.config import Config
    from sc_rpi.controllers import HardwareController

LOGGER = logging.getLogger(__name__)

class AddSection(Command):
    """`add_section` command."""

    def __init__(
        self,
        command_name: str,
        config: Config,
        hw_controller: HardwareController,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_name (str): It should be the camelcase version of the class name.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.

        """
        super().__init__(command_name, config, hw_controller)
        arguments_schema = {
            "$schema": "https://json-schema.org/schema#",
            "$defs": {
                "section": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "integer",
                        },
                        "end": {
                            "type": "integer",
                        },
                        "color": {
                            "type": "string",
                            "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
                        },
                    },
                    "required": ["start", "end", "color"],
                },
            },
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/section"},
                },
            },
            "required": ["sections"],
        }
        self._validator = Draft7Validator(arguments_schema)

    def validate_arguments(self) -> None:
        """Validate command arguments."""
        errors = list(self._validator.iter_errors(self.args))
        if len(errors) > 0:
            raise ParseError(errors)
        self._test_overlapping([(s["start"], s["end"]) for s in self.args["sections"]])

    def run(self) -> Response:
        """Execute the command.

        :return Response:   Returns this object with result of the execution
        """
        section_ids = []
        try:
            for s in self.args["sections"]:
                color = hex_to_rgb(s["color"])
                color = (int(color[0]), int(color[1]), int(color[2]))
                new_section = self._hw_controller.new_section(
                    s["start"], s["end"], color,
                )
                section_ids.append(new_section.id)

            self._hw_controller.render()
            sections = self._hw_controller.list_sections()
            return ResponseOk(HTTPStatus.ACCEPTED, {"sections": map_sections(sections)})
        except KeyError as ex:
            LOGGER.warning("Rollback sections.")
            self._hw_controller.remove_sections(section_ids)
            raise ApiError from ex
        except Exception as ex:
            LOGGER.warning("Rollback sections.")
            self._hw_controller.remove_sections(section_ids)
            raise ApiError from ex

    def _test_overlapping(
        self, sections: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """Test section overlapping using the merge sort algorithm.

        Args:
            sections (list[tuple[int, int]]): sections to be probed

        Raises:
            ApiError: raises `ApiError` in case of error

        Returns:
            list[tuple[int, int]]: returns the same received list

        """
        if len(sections) > 1:
            result = []
            m = len(sections) // 2
            l1 = sections[:m]
            l2 = sections[m:]
            l1 = self._test_overlapping(l1)
            l2 = self._test_overlapping(l2)
            i = 0
            j = 0
            while i < len(l1) and j < len(l2):
                if (
                    l2[j][0] <= l1[i][0] <= l2[j][1]
                    or l2[j][0] <= l1[i][1] <= l2[j][1]
                    or (l1[i][0] <= l2[j][0] and l1[i][1] >= l2[j][1])
                ):
                    raise ApiError(
                        HTTPStatus.BAD_REQUEST,
                        ErrorCode.BAD_REQUEST,
                        "Some sections in the request are overlapping themselves.",
                    )
                if l1[i][1] < l2[j][0]:
                    result.append(l1[i])
                    i += 1
                else:
                    result.append(l2[j])
                    j += 1
            return result + l1[i:] + l2[j:]

        return sections
