"""Dataclasses used as the `data` field in command responses.

Module names should match with command names.
"""

from sc_rpi.models.responses.commands import get_config
from sc_rpi.models.responses.commands.status import Status

__all__ = ["Status", "get_config"]

# TODO: move help.py and version.py here
