"""Contains the `UseConfig` class."""

from __future__ import annotations

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.use_config.args import UseConfigArgs
from sc_rpi.utils.commands.config import apply_named_config
from sc_rpi.utils.commands.decorators import log_before_running


@dataclass
class UseConfig(Command[UseConfigArgs]):
    """`use_config` command: apply a saved named configuration."""

    command_args: UseConfigArgs | None = None

    command_name: str = "use_config"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        """
        Unlike `edit_section` or `turn_section_on` (mutate the live state, then
        render), this command replaces all sections, so it must leave everything
        unchanged on failure. `apply_named_config` uses
        `HardwareController.prepare_config` (builds and validates the new sections
        without changing any state) and `HardwareController.apply_prepared` (renders,
        then replaces the state) as its last call. A failure at any earlier point
        leaves nothing to roll back.
        """
        name = self.command_args.name if self.command_args is not None else None
        return apply_named_config(
            self._hw_controller,
            self.command_name,
            name,
            self._config.strip.default_section_brightness,
        )
