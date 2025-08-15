"""Contains the `VersionResp` class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VersionResp:
    """Includes different version numbers, such as the SC RPI version."""

    python_version: str

    sc_rpi_version: str
