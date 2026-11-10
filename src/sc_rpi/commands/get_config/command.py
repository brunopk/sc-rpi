"""Contains the `GetConfig` class."""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.get_config.args import GetConfigArgs
from sc_rpi.commands.results import Result

# Required for mashumaro (do not move to type checking section)
from sc_rpi.config import Config
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.config import store
from sc_rpi.utils.config.masking import mask_secrets
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC


@dataclass
class GetConfigResult(Result[Config]):
    """Contains a configuration (secret values masked)."""

    payload: Config

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: Config,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (Config): The configuration, with secret values masked.

        """
        super().__init__(status_code, command_name, payload, None)


@dataclass
class GetConfig(Command[GetConfigArgs]):
    """`get_config` command: return a saved configuration (secret values masked)."""

    command_args: GetConfigArgs | None = None

    command_name: str = "get_config"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        name = self.command_args.name if self.command_args is not None else None
        # Only reads the saved file: neither the strip nor the sections are touched
        config = store.load(store.validate_name(name))
        return {
            SC_RPI_RESULT_TOPIC: GetConfigResult(
                HTTPStatus.ACCEPTED,
                self.command_name,
                mask_secrets(config),
            ),
        }
