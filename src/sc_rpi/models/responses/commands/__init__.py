"""Dataclasses used as the `data` field in command responses.

Module names should match with command names.
"""

from sc_rpi.models.responses.commands.status import Status
from sc_rpi.models.responses.commands.version import Version

__all__ = ["Status", "Version"]
