"""Contains the `TestGetConfig` class."""

from __future__ import annotations

from unittest.mock import patch

from sc_rpi.commands.base import Command
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color
from sc_rpi.utils.config.masking import SECRET_PLACEHOLDER
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC
from test.config_dir_test import ConfigDirTest, make_section


class TestGetConfig(ConfigDirTest):
    """Tests for `get_config` command."""

    def test_after_edit_section_shows_edited_section(self) -> None:
        """The running config is returned, not the initial values."""
        section_id = self.config.strip.sections[0].id
        self.hw_controller.edit_section(section_id, None, None, (1, 2, 3))
        payload = self._run()[SC_RPI_RESULT_TOPIC].to_dict()["payload"]
        section = next(s for s in payload["strip"]["sections"] if s["id"] == section_id)
        self.assertEqual({"r": 1, "g": 2, "b": 3}, section["color"])

    def test_basic_invocation(self) -> None:
        """Result keys, broker, masked password, sections and description."""
        result = self._run()
        payload = result[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, payload.status)
        self.assertEqual("get_config", payload.command_name)
        data = self._run()[SC_RPI_RESULT_TOPIC].to_dict()["payload"]
        self.assertIn("mqtt", data)
        self.assertIn("strip", data)
        self.assertEqual("homeassistant.local", data["mqtt"]["broker"]["host"])
        self.assertEqual(1883, data["mqtt"]["broker"]["port"])
        self.assertEqual(SECRET_PLACEHOLDER, data["mqtt"]["broker"]["password"])
        self.assertEqual("test", data["mqtt"]["broker"]["username"])
        for section in data["strip"]["sections"]:
            self.assertIn("color", section)
            self.assertFalse(section["is_on"])
        self.assertEqual("", data["description"])

    def test_description_of_running_config(self) -> None:
        """The description of the running config is returned."""
        self._save_config("party", [make_section("p1", 0, 9)], "Friday lights")
        Command.from_dict_wrapper(
            {"command_name": "use_config", "command_args": {"name": "party"}},
            self.config,
            self.hw_controller,
        ).run()
        data = self._run()[SC_RPI_RESULT_TOPIC].to_dict()["payload"]
        self.assertEqual("Friday lights", data["description"])

    def test_invalid_name(self) -> None:
        """A path-like name gives INVALID_CONFIG_NAME."""
        self._assert_code(ErrorCode.INVALID_CONFIG_NAME, {"name": "../config"})

    def test_no_file_changed(self) -> None:
        """`get_config`, with or without a name, does not touch `config/`."""
        self._save_config("party", [make_section("p1", 0, 9)])
        before = self._files()
        self._run()
        self._run({"name": "party"})
        self.assertEqual(before, self._files())

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the earlier change for A and unchanged values for B.

        A is the section changed earlier by `edit_section`; B is a section not modified.
        """
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        self.hw_controller.edit_section(a_id, None, None, (4, 5, 6))
        payload = self.run_command("get_config")[SC_RPI_RESULT_TOPIC].payload
        result_sections = {s.id: s for s in payload.strip.sections}
        self.assertEqual(Color(4, 5, 6), result_sections[a_id].color)
        self.assert_other_sections_unchanged(result_sections, {a_id})

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

    def _assert_code(self, code: ErrorCode, args: dict) -> None:
        """Assert that the command raises `code`."""
        with self.assertRaises(ApiError) as ctx:
            self._run(args)
        self.assertEqual(code, ctx.exception.code)

    def _run(self, args: dict | None = None) -> dict:
        """Run `get_config` and return its result."""
        return self.run_command("get_config", args)
