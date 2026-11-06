"""Contains `ConfigDirTest`, a base for tests that need a temporary `config/`."""

from __future__ import annotations

import os
import tempfile
from dataclasses import replace
from pathlib import Path
from unittest import TestCase

import yaml

from sc_rpi.config.strip import Section
from sc_rpi.controllers.hardware_controller import HardwareController
from sc_rpi.models import Color
from sc_rpi.utils.config import load_configurations, store


def make_section(
    section_id: str, start: int, end: int, *, is_on: bool = True,
) -> Section:
    """Build a config section."""
    return Section(
        color=Color(0, 255, 0),
        end=end,
        id=section_id,
        is_on=is_on,
        name=section_id.upper(),
        start=start,
    )


class ConfigDirTest(TestCase):
    """Runs in an empty temporary working directory with a `config/` folder."""

    def setUp(self) -> None:
        """Load the test config, then move to a temporary directory."""
        self.config = load_configurations("config_test.yaml")
        self.hw_controller = HardwareController(self.config)
        self._old_cwd = Path.cwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        Path("config").mkdir()

    def tearDown(self) -> None:
        """Restore the working directory."""
        os.chdir(self._old_cwd)
        self._tmp.cleanup()

    def _files(self) -> dict[str, bytes]:
        """Return the content of every file in `config/`."""
        return {p.name: p.read_bytes() for p in Path("config").iterdir()}

    def _save_config(
        self, name: str, sections: list[Section], description: str = "",
    ) -> None:
        """Write `config/<name>.yaml` with the given sections."""
        strip = replace(self.config.strip, sections=sections)
        config = replace(self.config, strip=strip, description=description)
        path = store.CONFIG_DIR / f"{name}.yaml"
        path.write_text(yaml.safe_dump(config.to_dict(), sort_keys=False))
