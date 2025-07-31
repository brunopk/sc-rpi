"""Contains the `TestTurnSectionOn` class."""

import logging
from unittest import TestCase

from sc_rpi.commands import add_section, turn_section_on
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response, Section
from sc_rpi.utils.config import load_configurations


class TestTurnSectionOn(TestCase):
    """Tests `turn_section_on` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
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

        command = Command.from_dict_wrapper(
            {"name": "turn_section_on", "args": {"section_id": first_section.id}},
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        try:
            resp = command.run()
        except Exception as ex:
            print(ex)
            raise ex
        self.assertIsInstance(resp, Response)
