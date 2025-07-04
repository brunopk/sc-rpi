"""Contains the Section class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Versions:
    """Includes different version numbers, such as the SC RPI version."""

    python_version: str

    sc_rpi_version: str
