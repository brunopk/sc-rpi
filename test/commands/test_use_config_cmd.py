"""Contains the `TestUseConfig` class."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from sc_rpi.commands.base import Command
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.commands.config import apply_named_config
from sc_rpi.utils.topics import (
    SC_RPI_RESULT_TOPIC,
    build_ha_availability_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
)
from test.config_dir_test import ConfigDirTest, make_section


class TestUseConfig(ConfigDirTest):
    """Tests for `use_config` command and `apply_named_config`."""

    def test_description_loaded(self) -> None:
        """The description of the config becomes the running one."""
        self._save_config("party", [make_section("p1", 0, 9)], "Friday lights")
        self._use({"name": "party"})
        self.assertEqual(
            "Friday lights", self.hw_controller.get_current_config().description,
        )

    def test_failure_building_result_leaves_state(self) -> None:
        """A failure before applying leaves controller and strip untouched."""
        self._save_config("night", [make_section("night_1", 0, 9)])
        before = self.hw_controller.list_sections()
        with (
            patch(
                "sc_rpi.utils.commands.config.build_ha_refresh_messages",
                side_effect=RuntimeError("boom"),
            ),
            patch.object(self.hw_controller, "_render") as render,
            self.assertRaises(RuntimeError),
        ):
            apply_named_config(self.hw_controller, "use_config", "night", 100)
        render.assert_not_called()
        self.assertEqual(before, self.hw_controller.list_sections())

    def test_helper_result_order_and_no_command(self) -> None:
        """The helper works without a command; SC RPi result is first."""
        self._save_config("night", [make_section("night_1", 0, 9)])
        result = apply_named_config(self.hw_controller, "use_config", "night", 100)
        keys = list(result)
        self.assertEqual(SC_RPI_RESULT_TOPIC, keys[0])
        self.assertEqual(
            [
                build_ha_discovery_topic("night_1"),
                build_ha_availability_topic("night_1"),
                build_ha_state_topic("night_1"),
            ],
            [k for k in keys if "night_1" in k],
        )
        offline = [k for k in keys[1:] if result[k] == "offline"]
        self.assertEqual(keys[1 : 1 + len(offline)], offline)

    def test_invalid_name(self) -> None:
        """A path-like name gives INVALID_CONFIG_NAME."""
        self._assert_code(ErrorCode.INVALID_CONFIG_NAME, {"name": "../config"})

    def test_missing_name(self) -> None:
        """No name gives MISSING_CONFIG_NAME."""
        self._assert_code(ErrorCode.MISSING_CONFIG_NAME, None)
        self._assert_code(ErrorCode.MISSING_CONFIG_NAME, {})

    def test_mqtt_not_applied(self) -> None:
        """MQTT settings of the loaded config are ignored."""
        self._save_config("night", [make_section("night_1", 0, 9)])
        host = self.hw_controller.get_current_config().mqtt.broker.host
        path = self._config_dir() / "night.yaml"
        path.write_text(path.read_text().replace(host, "other.example"))
        self._use({"name": "night"})
        self.assertEqual(host, self.hw_controller.get_current_config().mqtt.broker.host)

    def test_no_file_changed(self) -> None:
        """Applying a config does not touch `config/`."""
        self._save_config("night", [make_section("night_1", 0, 9)])
        before = self._files()
        self._use({"name": "night"})
        self.assertEqual(before, self._files())

    def test_previous_entities_unavailable(self) -> None:
        """Previous entities are marked offline and new ones published."""
        self._save_config("night", [make_section("night_1", 0, 9)])
        previous = [s.id for s in self.hw_controller.list_sections()]
        result = self._use({"name": "night"})
        for section_id in previous:
            self.assertEqual("offline", result[build_ha_availability_topic(section_id)])
        self.assertIn(build_ha_discovery_topic("night_1"), result)
        self.assertEqual("online", result[build_ha_availability_topic("night_1")])
        self.assertIn(build_ha_state_topic("night_1"), result)

    def test_section_beyond_strip(self) -> None:
        """A section beyond the strip length gives INVALID_CONFIG."""
        self._save_config("long", [make_section("l1", 0, 300)])
        self._assert_code(ErrorCode.INVALID_CONFIG, {"name": "long"})

    def test_switch_config(self) -> None:
        """Sections of the saved config replace the running ones."""
        self._save_config("night", [make_section("night_1", 0, 9, is_on=False)])
        result = self._use({"name": "night"})
        sections = self.hw_controller.list_sections()
        self.assertEqual(["night_1"], [s.id for s in sections])
        self.assertFalse(sections[0].is_on)
        payload = result[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, payload.status)
        self.assertEqual("use_config", payload.command_name)
        self.assertEqual(
            [("night_1", 0, 9, False)],
            [(s.id, s.start, s.end, s.is_on) for s in payload.payload.sections],
        )

    def test_unknown_name(self) -> None:
        """An unknown name gives CONFIG_NOT_FOUND."""
        self._assert_code(ErrorCode.CONFIG_NOT_FOUND, {"name": "nope"})

    def test_unreadable_file(self) -> None:
        """An unparsable file gives INVALID_CONFIG."""
        (self._config_dir() / "bad.yaml").write_text("{ not: [valid")
        self._assert_code(ErrorCode.INVALID_CONFIG, {"name": "bad"})

    def _assert_code(self, code: ErrorCode, args: dict | None) -> None:
        """Assert that the command raises `code` and the state is unchanged."""
        before = self.hw_controller.list_sections()
        with self.assertRaises(ApiError) as ctx:
            self._use(args)
        self.assertEqual(code, ctx.exception.code)
        self.assertEqual(before, self.hw_controller.list_sections())

    def _config_dir(self) -> Path:
        """Return the config directory."""
        return Path("config")

    def _use(self, args: dict | None) -> dict:
        """Run `use_config` and return its result."""
        data = {"command_name": "use_config"}
        if args is not None:
            data["command_args"] = args
        command = Command.from_dict_wrapper(data, self.config, self.hw_controller)
        command.validate()
        return command.run()
