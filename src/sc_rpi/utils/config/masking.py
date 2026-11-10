"""Contains functions to hide secret configuration values."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sc_rpi.config import Config

SECRET_PLACEHOLDER = "********"  # noqa: S105 (placeholder, not a real password)

SECRET_PATHS: tuple[tuple[str, ...], ...] = (("mqtt", "broker", "password"),)
"""Location of every secret value in `Config`, as a path of attribute names.

To add a new secret, add its path here: no command can leak it by forgetting to hide it.
"""


def mask_secrets(config: Config) -> Config:
    """Return a copy of `config` with every secret value replaced by a placeholder.

    The secret values are listed in `SECRET_PATHS` (today only the MQTT password).
    All other values, including the MQTT username, are returned as they are.

    Args:
        config (Config): Configuration to mask. It is not modified.

    Returns:
        Config: A copy of the configuration without secret values.

    """
    for path in SECRET_PATHS:
        config = _replace_at(config, path, SECRET_PLACEHOLDER)
    return config


def _replace_at(obj: object, path: tuple[str, ...], value: object) -> object:
    """Return a copy of the dataclass `obj` with the attribute at `path` replaced."""
    name, *rest = path
    if rest:
        value = _replace_at(getattr(obj, name), tuple(rest), value)
    return replace(obj, **{name: value})
