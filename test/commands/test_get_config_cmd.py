"""Contains the `TestGetConfig` class."""

import logging
from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.models.commands.all.get_config.get_config_cmd import GetConfigCmd
from sc_rpi.models.commands.command import Command
from sc_rpi.utils.config import load_configurations


class TestGetConfig(TestCase):
    """Tests for `get_config` command."""

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
                "command_name": "get_config",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
