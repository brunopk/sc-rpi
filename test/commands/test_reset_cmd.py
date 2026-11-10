"""Contains the `TestReset` class."""

from __future__ import annotations

from pathlib import Path

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.topics import (
    SC_RPI_RESULT_TOPIC,
    build_ha_availability_topic,
    build_ha_state_topic,
)
from test.config_dir_test import ConfigDirTest, make_section


class TestReset(ConfigDirTest):
    """Tests for `reset` command."""

    def test_active_configuration_restored(self) -> None:
        """Reset without a name reloads the config loaded by `use_config`."""
        self._save_config("default", [make_section("d1", 0, 9)])
        self._save_config("night", [make_section("n1", 0, 9)])
        self.run_command("use_config", {"name": "night"})
        self.hw_controller.edit_section("n1", None, None, (1, 2, 3))

        self.run_command("reset")

        section = self.hw_controller.get_section("n1")
        self.assertEqual((0, 255, 0), section.color_list[0])
        self.assertEqual(["n1"], [s.id for s in self.hw_controller.list_sections()])
        self.assertEqual("night", self._status().active_configuration)

    def test_active_file_invalid(self) -> None:
        """An invalid active file fails and leaves the state and active name."""
        self._save_config("night", [make_section("n1", 0, 9)])
        self.run_command("use_config", {"name": "night"})
        Path("config/night.yaml").write_text("{ not: [valid")
        self._assert_unavailable(ErrorCode.INVALID_CONFIG)

    def test_active_file_missing(self) -> None:
        """A missing active file fails and leaves the state and active name."""
        self._save_config("night", [make_section("n1", 0, 9)])
        self.run_command("use_config", {"name": "night"})
        Path("config/night.yaml").unlink()
        self._assert_unavailable(ErrorCode.CONFIG_NOT_FOUND)

    def test_after_edits(self) -> None:
        """Edits and turn off are undone by reset."""
        self._save_config("default", [make_section("d1", 0, 9)])
        self.run_command("reset")
        self.hw_controller.edit_section("d1", None, None, (1, 2, 3))
        self.hw_controller.turn_section_off("d1")
        self.run_command("reset")
        section = self.hw_controller.get_section("d1")
        self.assertEqual((0, 255, 0), section.color_list[0])
        self.assertTrue(section.is_on)

    def test_identical_to_use_config(self) -> None:
        """Results match `use_config` except for `command_name`."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self.run_command("reset", {"name": "party"})
        reset_result = self.run_command("reset", {"name": "party"})
        use_config_result = self.run_command("use_config", {"name": "party"})
        self.assertEqual(list(reset_result), list(use_config_result))
        reset_status = reset_result.pop(SC_RPI_RESULT_TOPIC)
        use_config_status = use_config_result.pop(SC_RPI_RESULT_TOPIC)
        self.assertEqual("reset", reset_status.command_name)
        self.assertEqual("use_config", use_config_status.command_name)
        self.assertEqual(reset_status.payload, use_config_status.payload)
        # The remaining entries are the Home Assistant messages, which must match
        self.assertEqual(
            self._to_dicts(reset_result),
            self._to_dicts(use_config_result),
        )

    def test_named_reset_sets_active_configuration(self) -> None:
        """A named reset makes that name the one a reset without a name reloads."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self.run_command("reset", {"name": "party"})
        self.assertEqual("party", self._status().active_configuration)
        self.hw_controller.edit_section("p1", None, None, (1, 2, 3))

        self.run_command("reset")

        section = self.hw_controller.get_section("p1")
        self.assertEqual((0, 255, 0), section.color_list[0])

    def test_no_file_changed(self) -> None:
        """Reset, with or without a name, does not touch `config/`."""
        self._save_config("default", [make_section("d1", 0, 9)])
        self._save_config("party", [make_section("p1", 0, 9)])
        before = self._files()
        self.run_command("reset")
        self.run_command("reset", {"name": "party"})
        self.assertEqual(before, self._files())

    def test_previous_entities_unavailable(self) -> None:
        """Previous entities are marked offline."""
        self._save_config("default", [make_section("d1", 0, 9)])
        previous = [s.id for s in self.hw_controller.list_sections()]
        result = self.run_command("reset")
        for section_id in previous:
            self.assertEqual("offline", result[build_ha_availability_topic(section_id)])

    def test_result_matches_status(self) -> None:
        """The result payload is the same as the one of a `status` command."""
        self._save_config("default", [make_section("d1", 0, 9)])
        self._save_config("party", [make_section("p1", 0, 9)], "Friday lights")
        for args in (None, {"name": "party"}):
            with self.subTest(args=args):
                result = self.run_command("reset", args)
                self.assertEqual(202, result[SC_RPI_RESULT_TOPIC].status)
                self.assertEqual(
                    self.run_command("status")[SC_RPI_RESULT_TOPIC].payload,
                    result[SC_RPI_RESULT_TOPIC].payload,
                )

    def test_section_configured_off(self) -> None:
        """A section configured off is off, also in Home Assistant."""
        self._save_config("default", [make_section("d1", 0, 9, is_on=False)])
        result = self.run_command("reset")
        self.assertFalse(self.hw_controller.get_section("d1").is_on)
        state = result[build_ha_state_topic("d1")].state
        self.assertEqual("off", str(getattr(state, "value", state)).lower())

    def test_unknown_name(self) -> None:
        """An unknown name raises CONFIG_NOT_FOUND and changes nothing."""
        before = self.hw_controller.list_sections()
        with self.assertRaises(ApiError) as ctx:
            self.run_command("reset", {"name": "nope"})
        self.assertEqual(ErrorCode.CONFIG_NOT_FOUND, ctx.exception.code)
        self.assertEqual(before, self.hw_controller.list_sections())

    def test_with_saved_name(self) -> None:
        """Reset with a name behaves like use_config."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self.run_command("reset", {"name": "party"})
        self.assertEqual(["p1"], [s.id for s in self.hw_controller.list_sections()])

    def test_without_name(self) -> None:
        """Reset without a name applies `config/default.yaml`."""
        self._save_config("default", [make_section("d1", 0, 9)])
        result = self.run_command("reset")
        self.assertEqual(["d1"], [s.id for s in self.hw_controller.list_sections()])
        payload = result[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, payload.status)
        self.assertEqual("reset", payload.command_name)
        self.assertEqual(["d1"], [s.id for s in payload.payload.sections])

    def _assert_unavailable(self, code: ErrorCode) -> None:
        """Assert that `reset` without a name raises `code` and changes nothing."""
        before = self.hw_controller.list_sections()
        with self.assertRaises(ApiError) as ctx:
            self.run_command("reset")
        self.assertEqual(code, ctx.exception.code)
        self.assertEqual(before, self.hw_controller.list_sections())
        self.assertEqual("night", self._status().active_configuration)

    def _status(self):  # noqa: ANN202
        """Return the payload of a `status` command."""
        return self.run_command("status")[SC_RPI_RESULT_TOPIC].payload

    def _to_dicts(self, result: dict) -> dict:
        """Return the payloads of a result as dicts (strings are kept as they are)."""
        return {
            topic: payload.to_dict() if hasattr(payload, "to_dict") else payload
            for topic, payload in result.items()
        }
