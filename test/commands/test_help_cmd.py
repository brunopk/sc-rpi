"""Contains the `TestHelp` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest


class TestHelp(CommandTest):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command = Command.from_dict({"command_name": "help"})
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="help")
