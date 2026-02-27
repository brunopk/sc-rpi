"""Contains the `TestMashumaro` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.available.edit_section.command import EditSectionCmd
from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations

# TODO: document how to run tests

class TestMashumaro(TestCase):
    """Tests serializing/deserializing objects.

    All subclasses must be imported before using them in order for mashumaro \
    discriminators to work correctly (even if only one of them is used)
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(cls.config)


    def test_deserializing_json(self):
        """test_deserializing_json."""
        json_data = {
            "command_name": "edit_section",
            "command_args": {
                "section_id": "xx",
                "start": 0,
                "end": 50,
                "color": {"r": 100, "g": 100, "b": 100},
            },
        }
        cmd = Command.from_dict_wrapper(
            json_data,
            self.__class__.config,
            self.__class__.hw_controller,
        )
        self.assertIsInstance(cmd, Command)
