"""Contains the `TestEditSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.edit_section import EditSectionCmd
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response
from sc_rpi.utils.config import load_configurations


class TestEditSection(TestCase):
    """Tests for `edit_section` command."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        new_section = self.__class__.hw_controller.new_section(0, 10, (255, 255, 0))

        section_edit_cmd = Command.from_dict_wrapper(
            {
                "name": "edit_section",
                "args": {
                    "section_id": new_section.id,
                    "start": 10,
                },
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        section_edit_cmd.validate()
        resp = section_edit_cmd.run()

        self.assertIsInstance(resp, Response)
