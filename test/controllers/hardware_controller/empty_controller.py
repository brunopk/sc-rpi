"""Contains `empty_hardware_controller`, used by hardware controller tests."""

from __future__ import annotations

from dataclasses import replace

from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations


def empty_hardware_controller() -> HardwareController:
    """Build a `HardwareController` from `config_test.yaml` without sections."""
    config = load_configurations("config_test.yaml")
    strip = replace(config.strip, sections=[])
    return HardwareController(replace(config, strip=strip))
