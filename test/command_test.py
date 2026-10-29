"""Contains the `CommandTest` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from unittest import TestCase

if TYPE_CHECKING:
    from sc_rpi.commands.base import CommandResult

from sc_rpi.commands.results import Result
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.topic_utils import (
    matches_ha_state_topic,
    matches_sc_rpi_result_topic,
)


class CommandTest(TestCase):
    """Used to test commands in sc_rpi.commands package.

    Contains common initializations.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations("config_test.yaml")
        cls.hw_controller = HardwareController(cls.config)

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
