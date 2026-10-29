"""Contains the `TestVersion` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest

class TestVersion(CommandTest):
    """Tests for `version` command."""

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "version",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="version")
