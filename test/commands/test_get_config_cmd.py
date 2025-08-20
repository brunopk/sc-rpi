"""Contains the `TestGetConfig` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.get_config import GetConfigCmd
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
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
        cmd = Command.from_dict_wrapper(
            {
                "name": "get_config",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        cmd.validate()
        resp = cmd.run()

        self.assertTrue(len(resp.payload.strip_config.sections) > 0)
        self.assertIsInstance(resp.to_json(), str)
        self.assertEqual(resp.command_name, GetConfigCmd.name)
