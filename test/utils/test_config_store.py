"""Tests for `sc_rpi.utils.config.store`."""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path
from unittest import TestCase

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.config import load_configurations, store


class TestConfigStore(TestCase):
    """Tests for the named config store (run in a temporary working directory)."""

    def setUp(self) -> None:
        """Load the test config, then move to an empty temporary directory."""
        self.config = load_configurations("config_test.yaml")
        self._old_cwd = Path.cwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        Path("config").mkdir()

    def tearDown(self) -> None:
        """Restore the working directory."""
        os.chdir(self._old_cwd)
        self._tmp.cleanup()

    @staticmethod
    def listing() -> list[str]:
        """Return the sorted file names in `config/`."""
        return sorted(p.name for p in Path("config").iterdir())

    def assert_code(self, code: ErrorCode, func, *args) -> None:  # noqa: ANN001, ANN002
        """Assert that `func(*args)` raises an `ApiError` with `code`."""
        with self.assertRaises(ApiError) as ctx:
            func(*args)
        self.assertEqual(code, ctx.exception.code)

    # validate_name / path_for / load

    def test_invalid_names(self) -> None:
        """Names outside the alphabet or length are rejected."""
        for name in ["../secret", "a/b", "a\\b", ".", "..", "a.b", "a" * 65, " x"]:
            with self.subTest(name=name):
                self.assert_code(
                    ErrorCode.INVALID_CONFIG_NAME, store.validate_name, name,
                )

    def test_missing_name(self) -> None:
        """A missing or empty name has its own code."""
        self.assert_code(ErrorCode.MISSING_CONFIG_NAME, store.validate_name, None)
        self.assert_code(ErrorCode.MISSING_CONFIG_NAME, store.validate_name, "")

    def test_valid_names(self) -> None:
        """Plain names are accepted."""
        for name in ["party", "Night-2", "a_b", "a" * 64]:
            with self.subTest(name=name):
                self.assertEqual(name, store.validate_name(name))
        self.assertEqual(Path("config/party.yaml"), store.path_for("party"))

    def test_load_missing(self) -> None:
        """Loading an unknown name fails with CONFIG_NOT_FOUND."""
        self.assert_code(ErrorCode.CONFIG_NOT_FOUND, store.load, "nope")

    def test_load_unparsable(self) -> None:
        """Loading an unparsable file fails with INVALID_CONFIG."""
        Path("config/bad.yaml").write_text("a: [unclosed")
        self.assert_code(ErrorCode.INVALID_CONFIG, store.load, "bad")

    # save

    def test_save_new_and_round_trip(self) -> None:
        """A saved config loads back equal to the original."""
        self.config.description = "Friday lights"
        self.config.strip.sections[0].is_on = True
        self.config.strip.sections[1].color.r = 0
        self.config.strip.sections[1].color.b = 0

        store.save("party", self.config)

        self.assertEqual(self.config, store.load("party"))

    def test_save_existing_keeps_file(self) -> None:
        """Saving an existing name fails and leaves the file unchanged."""
        store.save("party", self.config)
        before = Path("config/party.yaml").read_bytes()
        self.config.description = "other"

        self.assert_code(
            ErrorCode.CONFIG_ALREADY_EXISTS, store.save, "party", self.config,
        )

        self.assertEqual(before, Path("config/party.yaml").read_bytes())
        self.assertEqual(["party.yaml"], self.listing())

    def test_save_reserved_name(self) -> None:
        """`default` is rejected on save, case-insensitively, but can be loaded."""
        for name in ["default", "Default", "DEFAULT"]:
            with self.subTest(name=name):
                self.assert_code(
                    ErrorCode.RESERVED_CONFIG_NAME, store.save, name, self.config,
                )
        self.assertEqual([], self.listing())

        source = self._old_cwd / "config_test.yaml"
        Path("config/default.yaml").write_text(source.read_text())
        self.assertEqual(self.config, store.load("default"))

    def test_save_file_mode_and_no_temp_files(self) -> None:
        """Saved files are 0600 and no temporary file is left behind."""
        store.save("party", self.config)

        mode = stat.S_IMODE(Path("config/party.yaml").stat().st_mode)
        self.assertEqual(0o600, mode)
        self.assertEqual(["party.yaml"], self.listing())

    def test_save_invalid_name_writes_nothing(self) -> None:
        """An invalid name writes no file."""
        self.assert_code(ErrorCode.INVALID_CONFIG_NAME, store.save, "../x", self.config)
        self.assertEqual([], self.listing())
