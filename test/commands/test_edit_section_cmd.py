"""Contains the `TestEditSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.available.edit_section.command import EditSectionCmd
from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations

# TODO: add a test to set color

# TODO: set log level to info for all tests

class TestEditSection(TestCase):
    """Tests for `edit_section` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
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
                "command_name": "edit_section",
                "command_args": {
                    "section_id": new_section.id,
                    "end": 298,
                },
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
