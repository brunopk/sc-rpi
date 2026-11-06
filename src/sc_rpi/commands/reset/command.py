"""Contains the `Reset` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.reset.args import ResetArgs
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.named_config import apply_named_config
from sc_rpi.utils.config.store import DEFAULT_NAME


@dataclass
class Reset(Command[ResetArgs]):
    """`reset` command: apply `config/default.yaml`, or the saved config `name`.

    Unlike `edit_section` or `turn_section_on` (mutate the live state, then render),
    this command replaces all sections, so it must leave everything unchanged on
    failure. It uses `HardwareController.prepare_config` (builds and validates the new
    sections without changing any state) and `HardwareController.apply_prepared`
    (renders, then replaces the state), the last call of `run()`. A failure at any
    earlier point leaves nothing to roll back.
    """

    command_args: ResetArgs | None = None

    command_name: str = "reset"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        name = self.command_args.name if self.command_args is not None else None
        return apply_named_config(
            self._hw_controller,
            self.command_name,
            DEFAULT_NAME if name is None else name,
            self._config.strip.default_section_brightness,
        )
