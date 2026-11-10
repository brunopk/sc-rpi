"""Contains the `TestTurnSectionOn` class."""

import logging

from sc_rpi.commands.base import Command
from sc_rpi.models import Color
from test.command_test import CommandTest

# TODO: move all logging.basicConfig out of test case classes

logging.basicConfig(level=logging.DEBUG)

class TestTurnSectionOn(CommandTest):
    """Tests `turn_section_on` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        new_section = self.hw_controller.new_section(
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
            self.config,
            self.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="turn_section_on")

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the change for A and unchanged values for B.

        A is the section changed by `turn_section_on`; B is a section not modified.
        """
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        result = self.run_command(
            "turn_section_on",
            {"section_id": a_id, "color": {"r": 4, "g": 5, "b": 6}},
        )
        result_sections = self.get_result_sections(result)
        self.assertTrue(result_sections[a_id].is_on)
        self.assertEqual(Color(4, 5, 6), result_sections[a_id].color)
        self.assert_other_sections_unchanged(result_sections, {a_id})
