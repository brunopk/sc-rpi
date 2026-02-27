"""Contains the `TestStatus` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.available.status.status_cmd import StatusCmd
from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations


class TestStatus(TestCase):
    """Tests for `add_section` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "status",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
