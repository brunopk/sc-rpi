"""Contains the `TestVersion` class."""

from sc_rpi.commands.base import Command
from test.command_test_case import CommandTestCase

# TODO: CONTINUE validate that commands returns a dictionary and each entry is an instance of ScRpiResult or HAState (this could be a helper function) if it is instance of sc_rpi result validate that the command name is the corresponding command name

class TestVersion(CommandTestCase):
    """Tests for `add_section` command."""

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
        command.run()
