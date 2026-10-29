"""Contains the `TestStatus` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest


class TestStatus(CommandTest):
    """Tests for `status` command."""

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "status",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="status")
