"""Contains the `TestMashumaro` class."""

from unittest import TestCase

from sc_rpi.commands import *
from sc_rpi.models.command import Command


class TestMashumaro(TestCase):
    """Tests serializing/deserializing objects.

    All subclasses must be imported before using them in order for mashumaro \
    discriminators to work correctly (even if only one of them is used)
    """

    def test_deserializing_json(self):
        """Test test_deserializing_json."""
        json_data = {
            "name": "add_section",
            "args": {"start": 0, "end": 50, "color": "#aa22bb"},
        }
        cmd = Command.from_dict(json_data)
        self.assertIsInstance(cmd, Command)
