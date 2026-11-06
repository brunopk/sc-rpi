"""Contains the `TestReset` class."""

from __future__ import annotations

from sc_rpi.commands.base import Command
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

    def test_after_edits(self) -> None:
        """Edits and turn off are undone by reset."""
        self._save_config("default", [make_section("d1", 0, 9)])
        self._run_cmd("reset")
        self.hw_controller.edit_section("d1", None, None, (1, 2, 3))
        self.hw_controller.turn_section_off("d1")
        self._run_cmd("reset")
        section = self.hw_controller.get_section("d1")
        self.assertEqual((0, 255, 0), section.color_list[0])
        self.assertTrue(section.is_on)

    def test_identical_to_use_config(self) -> None:
        """Results match `use_config` except for `command_name`."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self._run_cmd("reset", {"name": "party"})
        reset = self._run_cmd("reset", {"name": "party"})
        use = self._run_cmd("use_config", {"name": "party"})
        self.assertEqual(list(reset), list(use))
        a, b = reset.pop(SC_RPI_RESULT_TOPIC), use.pop(SC_RPI_RESULT_TOPIC)
        self.assertEqual("reset", a.command_name)
        self.assertEqual("use_config", b.command_name)
        self.assertEqual(a.payload, b.payload)
        self.assertEqual(
            {k: v.to_dict() if hasattr(v, "to_dict") else v for k, v in reset.items()},
            {k: v.to_dict() if hasattr(v, "to_dict") else v for k, v in use.items()},
        )

    def test_previous_entities_unavailable(self) -> None:
        """Previous entities are marked offline."""
        self._save_config("default", [make_section("d1", 0, 9)])
        previous = [s.id for s in self.hw_controller.list_sections()]
        result = self._run_cmd("reset")
        for section_id in previous:
            self.assertEqual("offline", result[build_ha_availability_topic(section_id)])

    def test_section_configured_off(self) -> None:
        """A section configured off is off, also in Home Assistant."""
        self._save_config("default", [make_section("d1", 0, 9, is_on=False)])
        result = self._run_cmd("reset")
        self.assertFalse(self.hw_controller.get_section("d1").is_on)
        state = result[build_ha_state_topic("d1")].state
        self.assertEqual("off", str(getattr(state, "value", state)).lower())

    def test_unknown_name(self) -> None:
        """An unknown name raises CONFIG_NOT_FOUND and changes nothing."""
        before = self.hw_controller.list_sections()
        with self.assertRaises(ApiError) as ctx:
            self._run_cmd("reset", {"name": "nope"})
        self.assertEqual(ErrorCode.CONFIG_NOT_FOUND, ctx.exception.code)
        self.assertEqual(before, self.hw_controller.list_sections())

    def test_with_saved_name(self) -> None:
        """Reset with a name behaves like use_config."""
        self._save_config("party", [make_section("p1", 0, 9)])
        self._run_cmd("reset", {"name": "party"})
        self.assertEqual(["p1"], [s.id for s in self.hw_controller.list_sections()])

    def test_without_name(self) -> None:
        """Reset without a name applies `config/default.yaml`."""
        self._save_config("default", [make_section("d1", 0, 9)])
        result = self._run_cmd("reset")
        self.assertEqual(["d1"], [s.id for s in self.hw_controller.list_sections()])
        payload = result[SC_RPI_RESULT_TOPIC]
        self.assertEqual(202, payload.status)
        self.assertEqual("reset", payload.command_name)
        self.assertEqual(["d1"], [s.id for s in payload.payload.sections])

    def _run_cmd(self, name: str, args: dict | None = None) -> dict:
        """Run a command (`reset` or `use_config`) and return its result."""
        data = {"command_name": name}
        if args is not None:
            data["command_args"] = args
        command = Command.from_dict_wrapper(data, self.config, self.hw_controller)
        command.validate()
        return command.run()
