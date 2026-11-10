"""Contains the `TestStatus` class."""

from sc_rpi.commands.base import Command
from sc_rpi.models import Color
from test.command_test import CommandTest


class TestStatus(CommandTest):
    """Tests for `status` command."""

    def test_basic_invocation(self) -> None:
        """Basic test case."""
        command = Command.from_dict_wrapper(
            {
                "command_name": "status",
            },
            self.config,
            self.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="status")

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the earlier change for A and unchanged values for B.

        A is the section changed earlier by `edit_section`; B is a section not modified.
        """
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        self.hw_controller.edit_section(a_id, None, None, (4, 5, 6))
        result_sections = self.get_result_sections(self.run_command("status"))
        self.assertEqual(Color(4, 5, 6), result_sections[a_id].color)
        self.assert_other_sections_unchanged(result_sections, {a_id})
