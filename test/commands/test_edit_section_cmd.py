"""Contains the `TestEditSection` class."""

from sc_rpi.commands.base import Command
from sc_rpi.models import Color
from test.command_test import CommandTest

# TODO: add a test to set color

# TODO: set log level to info for all tests

class TestEditSection(CommandTest):
    """Tests for `edit_section` command."""

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
                "command_name": "edit_section",
                "command_args": {
                    "section_id": new_section.id,
                    "end": 298,
                },
            },
            self.config,
            self.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="edit_section")

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the edit for A and the running values for the others."""
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        result = self.run_command(
            "edit_section",
            {"section_id": a_id, "color": {"r": 4, "g": 5, "b": 6}},
        )
        sections = self.get_result_sections(result)
        self.assertEqual(Color(4, 5, 6), sections[a_id].color)
        self.assert_other_sections_unchanged(sections, {a_id})
