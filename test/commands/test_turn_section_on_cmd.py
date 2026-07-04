"""Contains the `TestTurnSectionOn` class."""

import logging

from sc_rpi.commands.base import Command
from test.command_test import CommandTest

# TODO: move all logging.basicConfig out of test case classes

logging.basicConfig(level=logging.DEBUG)

class TestTurnSectionOn(CommandTest):
    """Tests `turn_section_on` command."""

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
                "command_name": "turn_section_on",
                "command_args": {"section_id": new_section.id},
            },
            self.__class__.config,
            self.__class__.hw_controller,
        )
        command.validate()
        command.run()
