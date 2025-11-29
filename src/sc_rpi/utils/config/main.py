"""Contains helper functions."""

from __future__ import annotations

from pathlib import Path

import yaml
from RPi import GPIO

from sc_rpi.errors import ApiError
from sc_rpi.models.config import Config

"""Load all configurations from `config.ini` file."""

def load_configurations() -> Config:
    """Load all configurations from `config.ini` file.

    Raises:
        ApiException:

    Returns:
        Config: Return a `Config` instance with loaded configurations.

    """
    try:
        with Path.open(Path("config.yaml")) as f:
            config_dict = yaml.load(f, Loader=yaml.SafeLoader)
            return Config.from_dict(config_dict)
    except KeyError as ex:
        raise ApiError from ex
    except Exception as ex:
        raise ApiError from ex

def configure_status_led(config: Config):
    """Configure status led."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(config.status_led, GPIO.OUT)
