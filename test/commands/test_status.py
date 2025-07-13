"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.status import Status
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations


class TestStatus(TestCase):
    """Tests for src/commands/status.py."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(config=cls.config)

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        self.hw_controller.remove_all_sections()

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command = Status(None, config=self.config, hw_controller=self.hw_controller)
        command.validate()
        resp = command.run()

        self.assertIsInstance(resp, Response)

