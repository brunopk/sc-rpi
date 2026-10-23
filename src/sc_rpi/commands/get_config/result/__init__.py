"""Contains models with the same structure as in `/src/sc_rpi/models/config`.

Some configurations fields may be hidden from users (not included in these models).
"""

from sc_rpi.commands.get_config.result import mqtt, strip
from sc_rpi.commands.get_config.result.main import (
    GetConfigResult,
    GetConfigResultPayload,
)

__all__ = ["GetConfigResult", "GetConfigResultPayload", "mqtt", "strip"]
