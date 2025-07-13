"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.add_section import AddSection
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations
from sc_rpi.errors import ApiError


class TestAddSection(TestCase):
    """Tests for src/commands/add_section.py."""

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
        """Basic test case."""
        command = AddSection(
            {
                "sections": [
                    {
                        "start": 0,
                        "end": 149,
                        "color": "#ff0000",
                    },
                ],
            },
            config=self.config,
            hw_controller=self.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assertIsInstance(result, Response)
