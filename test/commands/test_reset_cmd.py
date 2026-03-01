"""Contains the `TestReset` class."""

import logging
from unittest import TestCase

from sc_rpi.commands import Reset
from sc_rpi.commands.base import Command
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.utils.config import load_configurations


class TestReset(TestCase):
    """Tests for `reset` command."""

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
                "command_name": "reset",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
