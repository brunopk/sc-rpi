"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.get_config import GetConfig
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations


class TestGetConfig(TestCase):
    """Tests for src/commands/get_config.py."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(config=cls.config)

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command = GetConfig(None, config=self.config, hw_controller=self.hw_controller)
        command.validate()
        resp = command.run()
        self.assertIsInstance(resp, Response)

