"""Contains the `SaveConfig` class."""

from __future__ import annotations

from dataclasses import dataclass, replace
from http import HTTPStatus

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.commands.results import Result
from sc_rpi.commands.save_config.args import SaveConfigArgs

# Required for mashumaro (do not move to type checking section)
from sc_rpi.config import Config
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.config import store
from sc_rpi.utils.config.masking import mask_secrets
from sc_rpi.utils.topics import SC_RPI_RESULT_TOPIC


@dataclass
class SaveConfigResult(Result[Config]):
    """Contains the saved configuration (secret values masked)."""

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
            payload (Config): The saved configuration, with secret values masked.

        """
        super().__init__(status_code, command_name, payload, None)


@dataclass
class SaveConfig(Command[SaveConfigArgs]):
    """`save_config` command: save the running configuration under a name."""

    command_args: SaveConfigArgs | None = None

    command_name: str = "save_config"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        args = self.command_args if self.command_args is not None else SaveConfigArgs()

        # An omitted name means the active configuration, as if it had been given.
        name = (
            self._hw_controller.active_configuration if args.name is None else args.name
        )

        # Sections keep their ids and names (and are already ordered by start)
        config = replace(
            self._hw_controller.get_current_config(),
            description=args.description,
        )

        # Validates the name and saves the file (raises ApiError on failure)
        store.save(store.validate_name(name), config, overwrite=args.overwrite)

        return {
            SC_RPI_RESULT_TOPIC: SaveConfigResult(
                HTTPStatus.ACCEPTED,
                self.command_name,
                mask_secrets(config),
            ),
        }
