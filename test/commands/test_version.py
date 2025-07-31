"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands import version
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations


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
        cmd = Command.from_dict_wrapper(
            {
                "name": "version",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        cmd.validate()
        result = cmd.run()
        self.assertIsInstance(result, Response)
