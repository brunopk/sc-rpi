"""Contains the `TestTurnSectionOff` class."""

from sc_rpi.commands.base import Command
from test.command_test import CommandTest


class TestTurnSectionOff(CommandTest):
    """Tests `turn_section_off` command."""

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
                "command_name": "turn_section_off",
                "command_args": {"section_id": new_section.id},
            },
            self.config,
            self.hw_controller,
        )
        command.validate()
        result = command.run()
        self.assert_valid_command_result(result, expected_command_name="turn_section_off")

    def test_result_ignores_initial_config(self) -> None:
        """The result shows A off and the running values for the others."""
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        self.hw_controller.turn_section_on(a_id, (4, 5, 6))
        result = self.run_command("turn_section_off", {"section_id": a_id})
        sections = self.get_result_sections(result)
        self.assertFalse(sections[a_id].is_on)
        self.assert_other_sections_unchanged(sections, {a_id})
