"""Contains helper functions."""

from __future__ import annotations

from pathlib import Path

import yaml
from RPi import GPIO

from sc_rpi.config import Config
from sc_rpi.errors.api_error import ApiError

"""Load all configurations from `config.ini` file."""

def load_configurations(file: str = "config.yaml") -> Config:
    """Load all configurations from `config.yaml` file.

    Args:
        file (str): Configuration file (loaded from the current working directory).

    Raises:
        ApiException:

    Returns:
        Config: Return a `Config` instance with loaded configurations.

    """
    try:
        with Path.open(Path(file)) as f:
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
