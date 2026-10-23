"""Contains the `TestEditSection` class."""

from sc_rpi.commands.base import Command
from test.command_test_case import CommandTestCase

# TODO: add a test to set color

# TODO: set log level to info for all tests

class TestEditSection(CommandTestCase):
    """Tests for `edit_section` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        new_section = self.__class__.hw_controller.new_section(
            "s",
            200,
            299,
            (255, 255, 0),
        )

        command = Command.from_dict_wrapper(
            {
                "command_name": "edit_section",
                "command_args": {
                    "section_id": new_section.id,
                    "end": 298,
                },
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
