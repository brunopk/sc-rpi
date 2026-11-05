"""Contains helper functions."""

from __future__ import annotations

from http import HTTPStatus
from pathlib import Path

import yaml
from RPi import GPIO

from sc_rpi.config import Config
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError


def load_configurations(file: str | Path = "config/default.yaml") -> Config:
    """Load all configurations from a YAML file.

    Boot and `sc_rpi.utils.config.store.load` both use this function, so a config is
    parsed the same way everywhere.

    Args:
        file (str | Path): Configuration file (relative paths are resolved from the \
            current working directory).

    Raises:
        ApiError: With code `INVALID_CONFIG` if the file cannot be read or parsed.

    Returns:
        Config: Return a `Config` instance with loaded configurations.

    """
    try:
        with Path(file).open() as f:
            config_dict = yaml.load(f, Loader=yaml.SafeLoader)
            return Config.from_dict(config_dict)
    except Exception as ex:
        raise ApiError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ErrorCode.INVALID_CONFIG,
        ) from ex

def configure_status_led(config: Config):
    """Configure status led."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(config.status_led, GPIO.OUT)
