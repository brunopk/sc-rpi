"""Contains the `TestReset` class."""

from sc_rpi.commands.base import Command
from test.command_test_case import CommandTestCase


class TestReset(CommandTestCase):
    """Tests for `reset` command."""

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "reset",
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
