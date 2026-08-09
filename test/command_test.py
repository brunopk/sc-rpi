"""Contains the `CommandTest` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.base import CommandResult
from sc_rpi.commands.results import Result
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.topic_utils import matches_ha_state_topic, matches_sc_rpi_result_topic


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

    # TODO: CONTINUE
    # TODO: use this in all command tests

    def validateCommandResult(self, result: CommandResult):
        for topic, value in result.items():
            if matches_ha_state_topic(topic):
                self.assertIsInstance(value, HAState)
            elif matches_sc_rpi_result_topic(topic):
                self.assertIsInstance(value, Result)
            else:
                raise KeyError(f"Unrecognized topic {topic}".format(topic=topic))

__all__ = ["CommandTest"]
