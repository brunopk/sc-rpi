"""Contains the `TestGetConfig` class."""

from __future__ import annotations

from unittest.mock import patch

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.config.masking import SECRET_PLACEHOLDER
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC
from test.config_dir_test import ConfigDirTest, make_section


class TestGetConfig(ConfigDirTest):
    """Tests for `get_config` command."""

    def test_basic_invocation(self) -> None:
        """Result keys, broker, masked password, sections and description."""
        self._save_config("party", [make_section("p1", 0, 9, is_on=False)])
        result = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, result.status)
        self.assertEqual("get_config", result.command_name)
        data = result.to_dict()["payload"]
        self.assertIn("mqtt", data)
        self.assertIn("strip", data)
        self.assertEqual("homeassistant.local", data["mqtt"]["broker"]["host"])
        self.assertEqual(1883, data["mqtt"]["broker"]["port"])
        self.assertEqual(SECRET_PLACEHOLDER, data["mqtt"]["broker"]["password"])
        self.assertEqual("test", data["mqtt"]["broker"]["username"])
        section = data["strip"]["sections"][0]
        self.assertEqual({"r": 0, "g": 255, "b": 0}, section["color"])
        self.assertFalse(section["is_on"])
        self.assertEqual("", data["description"])

    def test_invalid_name(self) -> None:
        """A path-like name gives INVALID_CONFIG_NAME."""
        self._assert_code(ErrorCode.INVALID_CONFIG_NAME, {"name": "../config"})

    def test_missing_name(self) -> None:
        """No name gives MISSING_CONFIG_NAME and changes nothing."""
        before = self.hw_controller.list_sections()
        files = self._files()
        for args in (None, {}, {"name": None}):
            with self.subTest(args=args):
                self._assert_code(ErrorCode.MISSING_CONFIG_NAME, args)
        self.assertEqual(before, self.hw_controller.list_sections())
        self.assertEqual(files, self._files())

    def test_no_file_changed(self) -> None:
        """`get_config` does not touch `config/`."""
        self._save_config("party", [make_section("p1", 0, 9)])
        before = self._files()
        self._run({"name": "party"})
        self.assertEqual(before, self._files())

    def test_saved_config_is_not_applied(self) -> None:
        """Reading a saved config leaves the strip and sections unchanged."""
        self._save_config("party", [make_section("p1", 0, 9)])
        before = self.hw_controller.list_sections()
        with (
            patch.object(self.hw_controller, "prepare_config") as prepare,
            patch.object(self.hw_controller, "apply_prepared") as apply,
            patch.object(self.hw_controller, "_render") as render,
        ):
            self._run({"name": "party"})
        prepare.assert_not_called()
        apply.assert_not_called()
        render.assert_not_called()
        self.assertEqual(before, self.hw_controller.list_sections())
        self.assertEqual("default", self.hw_controller.active_configuration)

    def test_saved_config_is_returned_masked(self) -> None:
        """A saved config is returned with its description and masked password."""
        self._save_config("party", [make_section("p1", 0, 9)], "Friday lights")
        data = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].to_dict()["payload"]
        self.assertEqual("Friday lights", data["description"])
        self.assertEqual(["p1"], [s["id"] for s in data["strip"]["sections"]])
        self.assertEqual(SECRET_PLACEHOLDER, data["mqtt"]["broker"]["password"])

    def test_unknown_name(self) -> None:
        """An unknown name gives CONFIG_NOT_FOUND."""
        self._assert_code(ErrorCode.CONFIG_NOT_FOUND, {"name": "nope"})

    def _assert_code(self, code: ErrorCode, args: dict | None) -> None:
        """Assert that the command raises `code`."""
        with self.assertRaises(ApiError) as ctx:
            self._run(args)
        self.assertEqual(code, ctx.exception.code)

    def _run(self, args: dict | None = None) -> dict:
        """Run `get_config` and return its result."""
        return self.run_command("get_config", args)
