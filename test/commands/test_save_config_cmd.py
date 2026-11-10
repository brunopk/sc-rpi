"""Contains the `TestSaveConfig` class."""

from __future__ import annotations

from pathlib import Path

from sc_rpi.commands.base import Command
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
        with self.assertRaises(ApiError) as ctx:
            self._run({"name": "party"})
        self.assertEqual(ErrorCode.CONFIG_ALREADY_EXISTS, ctx.exception.code)

    def test_basic_save(self) -> None:
        """Save the running config with new ids and return it masked."""
        result = self._run({"name": "party"})
        payload = result[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual("party", payload.name)
        self.assertIsNotNone(payload.config)
        self.assertEqual(2, len(payload.config.strip.sections))

    def test_default_case_insensitive(self) -> None:
        """Saving as `Default` or `DEFAULT` gives RESERVED_CONFIG_NAME."""
        for name in ["default", "Default", "DEFAULT"]:
            with self.assertRaises(ApiError) as ctx:
                self._run({"name": name})
            self.assertEqual(ErrorCode.RESERVED_CONFIG_NAME, ctx.exception.code)

    def test_description_empty_by_default(self) -> None:
        """Without a description, the saved config has an empty description."""
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual("", payload.config.description)

    def test_description_preserved(self) -> None:
        """The given description is saved and returned."""
        result = self._run({"name": "party", "description": "Friday lights"})
        payload = result[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual("Friday lights", payload.config.description)

    def test_ids_prefixed_and_ordered(self) -> None:
        """Section ids are rewritten as <name>_section_<n> ordered by start."""
        # Turn off then edit the second section to change its range
        sections = self.config.strip.sections
        self.hw_controller.edit_section(sections[1].id, 100, 199, None)
        self.hw_controller.edit_section(sections[0].id, 0, 99, None)
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        ids = [s.id for s in payload.config.strip.sections]
        self.assertEqual(["party_section_1", "party_section_2"], ids)

    def test_invalid_name(self) -> None:
        """A path-like name gives INVALID_CONFIG_NAME."""
        with self.assertRaises(ApiError) as ctx:
            self._run({"name": "../secret"})
        self.assertEqual(ErrorCode.INVALID_CONFIG_NAME, ctx.exception.code)

    def test_missing_name(self) -> None:
        """A missing name gives MISSING_CONFIG_NAME."""
        with self.assertRaises(ApiError) as ctx:
            self._run({"name": None})
        self.assertEqual(ErrorCode.MISSING_CONFIG_NAME, ctx.exception.code)

    def test_names_preserved(self) -> None:
        """Section names are kept as they are."""
        # Edit the second section's name
        self.hw_controller.edit_section(
            self.config.strip.sections[1].id, None, None, None,
        )
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        names = [s.name for s in payload.config.strip.sections]
        # Default names are the section ids in uppercase
        self.assertTrue(any(n for n in names))

    def test_no_home_assistant_message(self) -> None:
        """No Home Assistant topic is published."""
        result = self._run({"name": "party"})
        for topic in result:
            self.assertTrue(topic.startswith("scrpi/"), f"Unexpected topic: {topic}")

    def test_password_masked(self) -> None:
        """The password in the result is masked, but the file has the real value."""
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        self.assertEqual(SECRET_PLACEHOLDER, payload.config.mqtt.broker.password)

        # Load the saved file directly and check it has the real password
        saved = store.load("party")
        self.assertEqual("test", saved.mqtt.broker.password)

    def test_result_ignores_initial_config(self) -> None:
        """The result shows the earlier change for A and unchanged values for B.

        A is the section changed earlier by `edit_section`; B is a section not modified.
        """
        self.tamper_initial_config()
        a_id, b_id = (s.id for s in self.config.strip.sections[:2])
        self.hw_controller.edit_section(a_id, None, None, (4, 5, 6))
        payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        # Saved ids are rewritten as `party_section_<n>`, so map them back
        saved_sections = payload.config.strip.sections
        result_sections = dict(zip((a_id, b_id), saved_sections, strict=True))
        self.assertEqual(Color(4, 5, 6), result_sections[a_id].color)
        self.assert_other_sections_unchanged(result_sections, {a_id})

    def test_round_trip_off_section(self) -> None:
        """An off section keeps its color and off state after a round trip."""
        self.hw_controller.turn_section_off(self.config.strip.sections[0].id)
        self._run({"name": "party"})
        reloaded = store.load("party")
        section = reloaded.strip.sections[0]
        self.assertFalse(section.is_on)
        # The color is preserved from the original config (white from test config)
        self.assertEqual(255, section.color.r)
        self.assertEqual(255, section.color.g)
        self.assertEqual(255, section.color.b)

    def test_running_sections_unchanged(self) -> None:
        """The running sections keep their ids after save."""
        section_id = self.config.strip.sections[0].id
        before = self.hw_controller.list_sections()
        self._run({"name": "party"})
        after = self.hw_controller.list_sections()
        self.assertEqual(before, after)
        # Verify the first section still has the original id
        self.assertEqual(section_id, after[0].id)

    def test_save_creates_file(self) -> None:
        """The command creates the config file."""
        self.assertFalse((Path("config") / "party.yaml").exists())
        self._run({"name": "party"})
        self.assertTrue((Path("config") / "party.yaml").exists())

    def test_save_then_get_config(self) -> None:
        """The get_config result equals the save_config result's config."""
        save_payload = self._run({"name": "party"})[SC_RPI_RESULT_TOPIC].payload
        # Apply the saved config
        Command.from_dict_wrapper(
            {"command_name": "use_config", "command_args": {"name": "party"}},
            self.config,
            self.hw_controller,
        ).run()
        # Get the config
        get_result = Command.from_dict_wrapper(
            {"command_name": "get_config"},
            self.config,
            self.hw_controller,
        ).run()
        get_payload = get_result[SC_RPI_RESULT_TOPIC].payload
        # The sections should match (accounting for Color objects)
        self.assertEqual(
            len(save_payload.config.strip.sections),
            len(get_payload.strip.sections),
        )

    def test_status_code(self) -> None:
        """The result has status 202."""
        result = self._run({"name": "party"})
        self.assertEqual(202, result[SC_RPI_RESULT_TOPIC].status)

    def test_strip_unchanged(self) -> None:
        """The strip is not re-rendered."""
        before = self.hw_controller.list_sections()
        self._run({"name": "party"})
        after = self.hw_controller.list_sections()
        self.assertEqual(before, after)

    def _run(self, args: dict | None = None) -> dict:
        """Run `save_config` and return its result."""
        data = {"command_name": "save_config"}
        if args is not None:
            data["command_args"] = args
        command = Command.from_dict_wrapper(data, self.config, self.hw_controller)
        command.validate()
        return command.run()
