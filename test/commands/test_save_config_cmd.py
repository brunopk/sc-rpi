"""Contains the `TestSaveConfig` class."""

from __future__ import annotations

from pathlib import Path

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color
from sc_rpi.utils.config import store
from sc_rpi.utils.config.masking import SECRET_PLACEHOLDER
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC
from test.config_dir_test import ConfigDirTest, make_section


class TestSaveConfig(ConfigDirTest):
    """Tests for `save_config` command."""

    def test_already_exists(self) -> None:
        """Saving with an existing name gives CONFIG_ALREADY_EXISTS."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self._assert_code(ErrorCode.CONFIG_ALREADY_EXISTS, {"name": "party"})

    def test_basic_save(self) -> None:
        """Save the running config and return it masked, as a flat payload."""
        result = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, result.status)
        self.assertEqual("save_config", result.command_name)
        self.assertEqual(2, len(result.payload.strip.sections))
        data = result.to_dict()["payload"]
        self.assertLessEqual({"mqtt", "strip", "description"}, set(data))
        self.assertNotIn("name", data)
        self.assertNotIn("config", data)

    def test_default_case_insensitive(self) -> None:
        """Saving as `Default` or `DEFAULT` gives RESERVED_CONFIG_NAME."""
        for name in ["default", "Default", "DEFAULT"]:
            self._assert_code(ErrorCode.RESERVED_CONFIG_NAME, {"name": name})
        self.assertEqual({}, self._files())

    def test_description_empty_by_default(self) -> None:
        """Without a description, the saved config has an empty description."""
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual("", payload.description)

    def test_description_preserved(self) -> None:
        """The given description is saved and returned."""
        result = self._run({"name": "party", "description": "Friday lights"})
        payload = result[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual("Friday lights", payload.description)
        self.assertEqual("Friday lights", store.load("party").description)

    def test_ids_and_names_kept(self) -> None:
        """Sections are saved with the ids and names they have, ordered by start."""
        expected = [(s.id, s.name) for s in self.config.strip.sections]
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual(expected, [(s.id, s.name) for s in payload.strip.sections])
        saved = store.load("party")
        self.assertEqual(expected, [(s.id, s.name) for s in saved.strip.sections])

    def test_invalid_name(self) -> None:
        """A path-like name gives INVALID_CONFIG_NAME."""
        self._assert_code(ErrorCode.INVALID_CONFIG_NAME, {"name": "../secret"})
        self.assertEqual({}, self._files())

    def test_name_omitted_default_is_active(self) -> None:
        """While `default` is active, an omitted name is RESERVED_CONFIG_NAME."""
        self._save_config("default", [make_section("d1", 0, 9)])
        before = self._files()
        for args in (None, {}, {"overwrite": False}, {"overwrite": True}):
            with self.subTest(args=args):
                self._assert_code(ErrorCode.RESERVED_CONFIG_NAME, args)
        self.assertEqual(before, self._files())

    def test_name_omitted_with_overwrite(self) -> None:
        """An omitted name with `overwrite` updates the active configuration's file."""
        self._activate("night")
        self.hw_controller.edit_section("n1", None, None, (1, 2, 3))

        result = self._run({"overwrite": True})[SC_RPI_RESULT_TOPIC]

        self.assertEqual(202, result.status)
        saved = store.load("night")
        self.assertEqual(Color(1, 2, 3), saved.strip.sections[0].color)
        self.assertEqual("night", self.hw_controller.active_configuration)

    def test_name_omitted_without_overwrite(self) -> None:
        """An omitted name without `overwrite` gives CONFIG_ALREADY_EXISTS."""
        self._activate("night")
        before = self._files()
        for args in (None, {"overwrite": False}):
            with self.subTest(args=args):
                self._assert_code(ErrorCode.CONFIG_ALREADY_EXISTS, args)
        self.assertEqual(before, self._files())

    def test_named_save_keeps_active_configuration(self) -> None:
        """Saving never changes the active configuration."""
        self._activate("night")
        self._run({"name": "party"})
        self.assertEqual("night", self.hw_controller.active_configuration)

    def test_no_home_assistant_message(self) -> None:
        """No Home Assistant topic is published."""
        result = self._run({"name": "party"})
        self.assertEqual([SC_RPI_RESULT_TOPIC], list(result))

    def test_overwrite_default_is_rejected(self) -> None:
        """`default` cannot be replaced, even with `overwrite`."""
        self._save_config("default", [make_section("d1", 0, 9)])
        before = self._files()
        for name in ["default", "Default"]:
            self._assert_code(
                ErrorCode.RESERVED_CONFIG_NAME, {"name": name, "overwrite": True},
            )
        self.assertEqual(before, self._files())

    def test_overwrite_existing(self) -> None:
        """With `overwrite`, an existing saved config is replaced."""
        self._save_config("party", [make_section("p1", 0, 9)], "old")
        before_sections = self.hw_controller.list_sections()

        result = self._run(
            {"name": "party", "description": "new", "overwrite": True},
        )

        self.assertEqual(202, result[SC_RPI_RESULT_TOPIC].status)
        saved = store.load("party")
        self.assertEqual("new", saved.description)
        self.assertEqual(
            [s.id for s in self.config.strip.sections],
            [s.id for s in saved.strip.sections],
        )
        self.assertEqual([SC_RPI_RESULT_TOPIC], list(result))
        self.assertEqual(before_sections, self.hw_controller.list_sections())

    def test_overwrite_false_or_omitted_keeps_file(self) -> None:
        """Without `overwrite`, an existing saved config is unchanged."""
        self._save_config("party", [make_section("p1", 0, 9)], "old")
        before = self._files()
        for args in ({"name": "party"}, {"name": "party", "overwrite": False}):
            with self.subTest(args=args):
                self._assert_code(ErrorCode.CONFIG_ALREADY_EXISTS, args)
        self.assertEqual(before, self._files())

    def test_overwrite_new_name(self) -> None:
        """`overwrite` on a new name saves it as usual."""
        self._run({"name": "party", "overwrite": True})
        self.assertTrue((Path("config") / "party.yaml").exists())

    def test_password_masked(self) -> None:
        """The password in the result is masked, but the file has the real value."""
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual(SECRET_PLACEHOLDER, payload.mqtt.broker.password)
        self.assertEqual("test", store.load("party").mqtt.broker.password)

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the earlier change for A and unchanged values for B.

        A is the section changed earlier by `edit_section`; B is a section not modified.
        """
        self.tamper_initial_config()
        a_id = self.config.strip.sections[0].id
        self.hw_controller.edit_section(a_id, None, None, (4, 5, 6))
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        result_sections = {s.id: s for s in payload.strip.sections}
        self.assertEqual(Color(4, 5, 6), result_sections[a_id].color)
        self.assert_other_sections_unchanged(result_sections, {a_id})

    def test_round_trip_off_section(self) -> None:
        """An off section keeps its color and off state after save and get_config."""
        self.hw_controller.turn_section_off(self.config.strip.sections[0].id)
        self._run({"name": "party"})
        reloaded = self.run_command("get_config", {"name": "party"})[
            SC_RPI_RESULT_TOPIC
        ].payload
        section = reloaded.strip.sections[0]
        self.assertFalse(section.is_on)
        # The color is preserved from the original config (white from test config)
        self.assertEqual(Color(255, 255, 255), section.color)

    def test_running_sections_unchanged(self) -> None:
        """The strip and the running sections are not changed by a save."""
        before = self.hw_controller.list_sections()
        self._run({"name": "party"})
        self.assertEqual(before, self.hw_controller.list_sections())

    def test_save_creates_file(self) -> None:
        """The command creates the config file."""
        self.assertFalse((Path("config") / "party.yaml").exists())
        self._run({"name": "party"})
        self.assertTrue((Path("config") / "party.yaml").exists())

    def test_save_then_get_config(self) -> None:
        """`get_config` with the saved name returns the `save_config` payload."""
        save_result = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC]
        get_result = self.run_command("get_config", {"name": "party"})[
            SC_RPI_RESULT_TOPIC
        ]
        self.assertEqual(save_result.payload, get_result.payload)
        self.assertEqual(
            save_result.to_dict()["payload"], get_result.to_dict()["payload"],
        )

    def _activate(self, name: str) -> None:
        """Save a config with section `n1` as `name` and make it the active one."""
        self._save_config(name, [make_section("n1", 0, 9)])
        self.run_command("use_config", {"name": name})
        self.assertEqual(name, self.hw_controller.active_configuration)

    def _assert_code(self, code: ErrorCode, args: dict | None) -> None:
        """Assert that the command raises `code`."""
        with self.assertRaises(ApiError) as ctx:
            self._run(args)
        self.assertEqual(code, ctx.exception.code)

    def _run(self, args: dict | None = None) -> dict:
        """Run `save_config` and return its result."""
        return self.run_command("save_config", args)
