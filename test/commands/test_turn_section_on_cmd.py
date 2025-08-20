"""Contains the `TestTurnSectionOn` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.turn_section_on import TurnSectionOnCmd
from sc_rpi.controllers import HardwareController
from sc_rpi.models import Response
from sc_rpi.models.command import Command
from sc_rpi.utils.config import load_configurations


class TestTurnSectionOn(TestCase):
    """Tests `turn_section_on` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        new_section = self.__class__.hw_controller.new_section(
            "s",
            200,
            299,
            (255, 255, 0),
        )

        command = Command.from_dict_wrapper(
            {"name": "turn_section_on", "args": {"section_id": new_section.id}},
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        resp = command.run()

        self.assertIsInstance(resp, Response)
        self.assertIsInstance(resp.to_json(), str)
        self.assertEqual(resp.command_name, TurnSectionOnCmd.name)
