"""Contains the `TestRemoveSections` class."""

import logging
from unittest import TestCase

from sc_rpi.commands import add_section, remove_sections
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response, Section
from sc_rpi.utils.config import load_configurations


class TestRemoveSections(TestCase):
    """Tests for `remove_sections` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        section_add_cmd = Command.from_dict_wrapper(
            {
                "name": "add_section",
                "args": [
                    {
                        "start": 0,
                        "end": 10,
                        "color": "#ffff00",
                    },
                ],
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        resp = section_add_cmd.run()

        if resp.payload is None:
            error_msg = '"payload" cannot be None'
            raise KeyError(error_msg)
        sections = resp.payload.sections
        if sections is None:
            error_msg = '"sections" cannot be None'
            raise KeyError(error_msg)
        first_section = sections[0]
        if not isinstance(first_section, Section):
            raise Exception("section[0] must be a Section instance")


        cmd = Command.from_dict_wrapper(
            {
                "name": "remove_sections",
                "args": [first_section.id]
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        cmd.validate()
        result = cmd.run()
        self.assertIsInstance(result, Response)
