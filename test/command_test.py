"""Contains the `CommandTest` class."""

import logging
from unittest import TestCase

from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.utils.config import load_configurations


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

__all__ = ["CommandTest"]
