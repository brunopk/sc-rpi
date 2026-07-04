"""Contains the `TestGetConfig` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest


class TestGetConfig(CommandTest):
    """Tests for `get_config` command."""

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "get_config",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
