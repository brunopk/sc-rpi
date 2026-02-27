"""Contains the `TestVersion` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.available.version.version_cmd import VersionCmd
from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations

# TODO: validate that commands returns a dictionary and each entry is an instance of ScRpiResult or HAState (this could be a helper function) if it is instance of sc_rpi result validate that the command name is the corresponding command name

class TestVersion(TestCase):
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
                "command_name": "version",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
