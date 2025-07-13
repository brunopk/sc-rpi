"""Contains the `Command` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sc_rpi.errors import ApiError, ParseError

if TYPE_CHECKING:

    from sc_rpi.config import Config
    from sc_rpi.controllers import HardwareController
    from sc_rpi.models.responses import Response


class Command:
    """Represents a command of SC RPI.

    To implement a command :

    1. Create the corresponding module in the commands package
    2. Create the class
    3. Define the `_DRAFT_VALIDATOR` class attribute \
        ([Draft specification](https://json-schema.org/specification))
    3. Re-implement the `run` method
    4. Re-implement `validate` method

    Important considerations:
    - The command class must inherit from `Command`
    - The class name must be the camelized version of the module name.
    - `validate` method validates arguments based on Draft specification defined in \
        `_DRAFT_VALIDATOR`, re-implement this method only if custom logic is needed, \
            otherwise re-implemented it with an empty body
    - `__init__` method must invoke the `__init__` method of `Command`
    - Command should not interact with MQTT, this is done by workers \
        (`src/sc_rpi/worker.py`).

    """

    def __init__(
        self,
        command_args: dict | None,
        config: Config,
        hw_controller: HardwareController,
    ) -> None:
        """Initialize the instance (constructor).

        Args:
            command_args (dict | None): Command arguments.
            config (Config): Configurations of SC RPI.
            hw_controller (HardwareController): Used to control the strip.

        """
        self._command_name = str(self.__module__)
        self._command_args = command_args
        self._config = config
        self._hw_controller = hw_controller

    @property
    def command_name(self) -> str:
        """Command name (snake-case version)."""
        return self._command_name

    def run(self) -> Response:
        """Execute the command.

        Returns:
            Response: Contains the result of the execution

        """
        raise NotImplementedError

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command

        Raises:
            ApiError:
            ParseError:

        """
        validator = getattr(self.__class__, "_DRAFT_VALIDATOR", None)
        if validator is None:
            msg = (
                "class attribute _DRAFT_VALIDATOR not defined in "
                 f"{self.__class__.__name__} class"
            )
            raise ApiError(message=msg)
        errors = [
            e.message for e in validator.iter_errors(self._command_args)
        ]
        if len(errors) > 0:
            raise ParseError(errors)
