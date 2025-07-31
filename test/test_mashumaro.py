"""Contains the `TestMashumaro` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.edit_section import EditSection
from sc_rpi.controllers import HardwareController
from sc_rpi.models.command import Command
from sc_rpi.utils.config import load_configurations


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
        """Test test_deserializing_json."""
        json_data = {
            "name": "edit_section",
            "args": {"section_id": "xx", "start": 0, "end": 50, "color": "#aa22bb"},
        }
        cmd = Command.from_dict_wrapper(
            json_data,
            self.__class__.config,
            self.__class__.hw_controller,
        )
        self.assertIsInstance(cmd, Command)
