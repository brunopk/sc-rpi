"""Contains the `TestHelp` class."""

from unittest import TestCase

from sc_rpi.models.commands.all.help.help_cmd import HelpCmd
from sc_rpi.models.commands.command import Command


class TestHelp(TestCase):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command =Command.from_dict({"command_name": "help"})
        command.validate()
        command.run()
