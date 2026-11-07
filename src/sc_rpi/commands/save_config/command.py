"""Contains the `SaveConfig` class."""

from __future__ import annotations

from dataclasses import dataclass, replace
from http import HTTPStatus

from mashumaro.mixins.json import DataClassJSONMixin

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
class SaveConfigPayload(DataClassJSONMixin):
    """Contains the saved config name and configuration (secret values masked)."""

    name: str

    config: Config


@dataclass
class SaveConfigResult(Result[SaveConfigPayload]):
    """Contains the saved config name and configuration (secret values masked)."""

    payload: SaveConfigPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: SaveConfigPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (SaveConfigPayload): Contains name and config with masked secrets.

        """
        super().__init__(status_code, command_name, payload, None)


@dataclass
class SaveConfig(Command[SaveConfigArgs]):
    """`save_config` command: save the current configuration under a name."""

    command_args: SaveConfigArgs | None = None

    command_name: str = "save_config"

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        name = self.command_args.name if self.command_args is not None else None
        description = (
            self.command_args.description if self.command_args is not None else ""
        )

        # Validate the name (raises ApiError on failure)
        store.validate_name(name)

        # Get the current config
        current_config = self._hw_controller.get_current_config()

        # Create a new config with updated section ids and description
        # Sort sections by start position and assign new ids
        sorted_sections = sorted(
            current_config.strip.sections,
            key=lambda s: s.start,
        )
        new_sections = [
            replace(
                section,
                id=f"{name}_section_{i + 1}",
            )
            for i, section in enumerate(sorted_sections)
        ]

        # Build the new config with updated sections and description
        new_config = replace(
            current_config,
            strip=replace(
                current_config.strip,
                sections=new_sections,
            ),
            description=description,
        )

        # Save the config (raises ApiError on failure)
        store.save(name, new_config)

        # Return the result with the masked config
        masked_config = mask_secrets(new_config)

        return {
            SC_RPI_RESULT_TOPIC: SaveConfigResult(
                HTTPStatus.ACCEPTED,
                self.command_name,
                SaveConfigPayload(name=name, config=masked_config),
            ),
        }
