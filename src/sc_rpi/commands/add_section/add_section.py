"""Contains the `AddSection` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from http import HTTPStatus

from webcolors import hex_to_rgb

from sc_rpi.commands.add_section.section import Section
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response, Status
from sc_rpi.utils import map_sections

logger = logging.getLogger(__name__)

@dataclass
class AddSection(Command[list[Section]]):
    """`add_section` command."""

    args: list[Section]

    name: str = "add_section"

    def run(self) -> Response:
        """Execute the command.

        :return Response: Contains the result of the execution
        """
        self._test_overlapping([(s.start, s.end) for s in self.args])
        section_ids = []

        try:
            for s in self.args:
                color = hex_to_rgb(s.color)
                color = (int(color[0]), int(color[1]), int(color[2]))
                new_section = self._hw_controller.new_section(s.start, s.end, color)
                section_ids.append(new_section.id)

            self._hw_controller.render()
            sections = self._hw_controller.list_sections()
            result = Status(map_sections(sections))

            return Response(HTTPStatus.ACCEPTED, result)
        except KeyError as ex:
            logger.warning("Rollback sections.")
            self._hw_controller.remove_sections(section_ids)
            raise ApiError from ex
        except Exception as ex:
            logger.warning("Rollback sections.")
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
