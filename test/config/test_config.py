"""Tests for `Config` loading."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

import yaml

from sc_rpi.utils.config import load_configurations


class TestConfig(TestCase):
    """Tests for `Config`."""

    def test_description_defaults_to_empty(self) -> None:
        """A file without description is still valid."""
        config = load_configurations("config_test.yaml")
        self.assertEqual("", config.description)

    def test_description_is_kept(self) -> None:
        """A file with a description keeps it."""
        data = yaml.safe_load(Path("config_test.yaml").read_text())
        data["description"] = "Friday lights"
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "with_description.yaml"
            path.write_text(yaml.safe_dump(data))
            config = load_configurations(str(path))
        self.assertEqual("Friday lights", config.description)