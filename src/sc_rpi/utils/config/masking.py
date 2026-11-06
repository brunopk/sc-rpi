"""Contains functions to hide secret configuration values."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sc_rpi.config import Config

SECRET_PLACEHOLDER = "********"  # noqa: S105 (placeholder, not a real password)


def mask_secrets(config: Config) -> Config:
    """Return a copy of `config` with every secret value replaced by a placeholder.

    The secret fields are listed in this function (today only the MQTT password).
    All other values, including the MQTT username, are returned as they are. To add
    a new secret, mask it here: no command can leak it by forgetting to hide it.

    Args:
        config (Config): Configuration to mask. It is not modified.

    Returns:
        Config: A copy of the configuration without secret values.

    """
    broker = replace(config.mqtt.broker, password=SECRET_PLACEHOLDER)
    mqtt = replace(config.mqtt, broker=broker)
    return replace(config, mqtt=mqtt)