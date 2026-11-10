"""Contains the `TestCommandDeserialization` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest


class TestCommandDeserialization(CommandTest):
    """Tests deserializing JSON into the right `Command` subclass.

    All subclasses must be imported before using them in order for mashumaro \
    discriminators to work correctly (even if only one of them is used)
    """

    def test_deserializing_json(self) -> None:
        """A JSON dict is deserialized into a `Command` through its discriminator."""
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
            self.config,
            self.hw_controller,
        )
        self.assertIsInstance(cmd, Command)
