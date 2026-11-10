"""Contains the `CommandTest` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from unittest import TestCase

if TYPE_CHECKING:
    from sc_rpi.commands.base import CommandResult

from sc_rpi.commands.base import Command
from sc_rpi.commands.results import Result
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.models import Color
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.topics import (
    SC_RPI_RESULT_TOPIC,
    matches_ha_state_topic,
    matches_sc_rpi_result_topic,
)

TAMPERED_COLOR = Color(9, 8, 7)


class CommandTest(TestCase):
    """Used to test commands in sc_rpi.commands package.

    Contains common initializations.
    """

    def setUp(self) -> None:
        """Load the test config and build a fresh controller for each test."""
        logging.basicConfig(level=None)
        self.config = load_configurations("config_test.yaml")
        self.hw_controller = HardwareController(self.config)
        # Running (color, is_on) by section id, saved by `tamper_initial_config`
        self._running_values: dict[str, tuple[Color, bool]] = {}

    def assert_other_sections_unchanged(
        self,
        sections: dict,
        changed_ids: set[str],
    ) -> None:
        """Check that the sections the command did not change keep their running values.

        The running values are the ones saved by `tamper_initial_config`, so a result
        built from the initial configuration (which that method tampered with) fails.

        Args:
            sections: Sections shown by a command result, by id (objects with `color`
                and `is_on`).
            changed_ids: Ids of the sections the test changed, which are not checked.

        """
        self.assertTrue(
            self._running_values, "call `tamper_initial_config` before the command"
        )
        for section_id, (color, is_on) in self._running_values.items():
            if section_id in changed_ids:
                continue
            self.assertEqual(color, sections[section_id].color, section_id)
            self.assertEqual(is_on, sections[section_id].is_on, section_id)

    def assert_valid_command_result(
        self, result: CommandResult, expected_command_name: str | None = None
    ) -> None:
        """Validate command result structure and types.

        For each topic in result:
        - If topic is HA state: payload must be HAState instance
        - If topic is SC RPi result: payload must be Result instance
        - If expected_command_name provided: validate Result.command_name matches

        Args:
            result: The CommandResult dict to validate
            expected_command_name: Optional command name to validate against
                Result entries

        Raises:
            AssertionError: If validation fails

        """
        for topic, payload in result.items():
            if matches_ha_state_topic(topic):
                self.assertIsInstance(
                    payload,
                    HAState,
                    f"Expected HAState for HA topic {topic}, "
                    f"got {type(payload).__name__}",
                )
            elif matches_sc_rpi_result_topic(topic):
                self.assertIsInstance(
                    payload,
                    Result,
                    f"Expected Result for SC RPi topic {topic}, "
                    f"got {type(payload).__name__}",
                )
                if expected_command_name is not None:
                    self.assertEqual(
                        payload.command_name,
                        expected_command_name,
                        f"Result command_name mismatch: "
                        f"expected '{expected_command_name}', "
                        f"got '{payload.command_name}'",
                    )
            else:
                self.fail(f"Unrecognized topic: {topic}")

    def get_result_sections(self, result: CommandResult) -> dict:
        """Return the sections of the SC RPi result of a command, by id."""
        return {s.id: s for s in result[SC_RPI_RESULT_TOPIC].payload.sections}

    def run_command(self, command_name: str, args: dict | None = None) -> CommandResult:
        """Build, validate and run a command.

        Args:
            command_name: Name of the command.
            args: Arguments of the command, if any.

        Returns:
            CommandResult: What `run()` returned.

        """
        data: dict = {"command_name": command_name}
        if args is not None:
            data["command_args"] = args
        command = Command.from_dict_wrapper(data, self.config, self.hw_controller)
        command.validate()
        return command.run()

    def tamper_initial_config(self) -> None:
        """Make the initial configuration differ from the running state.

        Saves the running color and on/off state of every section, then replaces them
        in the initial configuration (`hw_controller._config`) with `TAMPERED_COLOR`
        and `is_on=True`. A command whose result is built from the initial
        configuration instead of the running state then shows the tampered values.
        Check the result with `assert_other_sections_unchanged`.
        """
        for section in self.hw_controller.list_sections():
            self._running_values[section.id] = (
                Color(*section.color_list[0]),
                section.is_on,
            )
        for section in self.hw_controller._config.strip.sections:  # noqa: SLF001
            section.color = TAMPERED_COLOR
            section.is_on = True
        for color, is_on in self._running_values.values():
            self.assertNotEqual(TAMPERED_COLOR, color)
            self.assertFalse(is_on)
