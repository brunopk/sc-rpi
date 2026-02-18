"""Decorator factories for `Command` instances."""

from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Callable

from sc_rpi.models.commands.command import Command, CommandResult

if TYPE_CHECKING:
  from mashumaro.mixins.json import DataClassJSONMixin

LOGGER = logging.getLogger(__name__)

def log_call() -> Callable[
    [Callable[[object], CommandResult]],
    Callable[[object], CommandResult],
]:
    """Log the name of the command before executing it."""

    def decorator(
        run: Callable[[object], CommandResult],
    ) -> Callable[[object], CommandResult]:

        @wraps(run)
        def _wrapped_run_func(
            self: Command,
            *args: any,
            **kwargs: any
        ) -> dict[str, DataClassJSONMixin | str]:

            LOGGER.info("Executing %s command", self.command_name)
            return run(self, *args, **kwargs)

        return _wrapped_run_func

    return decorator
