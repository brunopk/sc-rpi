"""Contains the `TestTurnSectionOn` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.available.turn_section_on.turn_section_on_cmd import (
    TurnSectionOnCmd,
)
from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations

# TODO: move all logging.basicConfig out of test case classes

logging.basicConfig(level=logging.DEBUG)

class TestTurnSectionOn(TestCase):
    """Tests `turn_section_on` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        new_section = self.__class__.hw_controller.new_section(
            "s",
            200,
            299,
            (255, 255, 0),
        )

        command = Command.from_dict_wrapper(
            {
                "command_name": "turn_section_on",
                "command_args": {"section_id": new_section.id},
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
