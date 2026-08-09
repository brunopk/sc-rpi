"""Contains the `TestHelp` class."""

from sc_rpi.commands.base import Command
from test.command_test_case import CommandTestCase


class TestHelp(CommandTestCase):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command =Command.from_dict({"command_name": "help"})
        command.validate()
        command.run()
