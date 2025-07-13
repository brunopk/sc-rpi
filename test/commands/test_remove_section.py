"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.remove_section import RemoveSection
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations


class TestRemoveSection(TestCase):
    """Tests for src/commands/remove_section.py."""

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
        section_edit_cmd = RemoveSection(
            {
                "sections": [],
            },
            config=self.config,
            hw_controller=self.hw_controller,
        )
        section_edit_cmd.validate()
        resp = section_edit_cmd.run()

        self.assertIsInstance(resp, Response)

