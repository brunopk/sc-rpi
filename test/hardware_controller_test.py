"""Contains the `HardwareControllerTest` class."""

from __future__ import annotations

from dataclasses import replace
from unittest import TestCase

from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.utils.config import load_configurations


class HardwareControllerTest(TestCase):
    """Used to test `HardwareController` directly (not through a command).

    Each test gets a fresh controller, built from `config_test.yaml` without sections.
    """

    def setUp(self) -> None:
        """Build a controller without sections for each test."""
        config = load_configurations("config_test.yaml")
        strip = replace(config.strip, sections=[])
        self.controller = HardwareController(replace(config, strip=strip))
