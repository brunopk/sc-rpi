"""Contains the `Command` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Union

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from sc_rpi.controllers import HardwareController
from sc_rpi.models.config import Config

CommandArgs = TypeVar("CommandArgs")

CommandResult = dict[str, Union[DataClassJSONMixin, str]]

@dataclass
class Command(Generic[CommandArgs], DataClassJSONMixin):
    """Represents a command of SC RPi.

    **This class is not thead-safe**. Attributes such as `_config` may be shared \
        between a number of `Command` instances in different threads.

    To implement a command :

    1. Create the corresponding module in the `commands` package
    2. Create the main class for the command
        1. Re-implement the `run` method
        2. Re-implement `validate` method (if custom validation logic is needed)
    3. Create another class for command arguments


    Important considerations:
    - **The new class must inherit from `Command`.**
    - **The new class must contain the `name` class attribute** in order for the \
        Mashumaro discriminator to work correctly (discriminator is configured in the \
            `Config` class below).
    - The value for `name` should be the command name that API users will use when \
        invoking the command and it should be the snake-case version of the class name
    - Command should not interact with MQTT, this is done by workers \
        (`src/sc_rpi/worker.py`).
    - Use `from_dict_wrapper` instead of `from_dict` to create `Command` instances \
        from a dictionary. If some error occurs when using this method, Mashumaro will \
            raise `InvalidFieldValue`.
    - All subclasses must be imported before using them in order for mashumaro \
        discriminators to work correctly.
    - Do not use `to_dict`, this method will method will expose private class \
        attributes such as `_config`.

    """

    name: str

    args: Optional[CommandArgs] = None

    _config: Optional[Config] = None

    _hw_controller: Optional[HardwareController] = None

    class Config(BaseConfig):
        """Mashumaro config."""

        discriminator = Discriminator(
            field="name",
            include_subtypes=True,
        )

    @classmethod
    def from_dict_wrapper(
        cls,
        data: dict,
        config: Config,
        hw_controller: HardwareController,
    ) -> Command:
        """Generate a command instance from a dictionary representation of a command.

        This method wraps Mashumaro `from_dict` method.

        Args:
            data: dict: Dictionary from which to create the command.
            config (Config): SC RPi configuration. Take into account that `Command` is \
                not thead-safe (this `Config` instance may be shared between a number \
                    of `Command` instances in different threads).
            hw_controller (HardwareController): Used to interact with the hardware.

        """
        cmd = cls.from_dict(data)
        cmd._config = config
        cmd._hw_controller = hw_controller
        return cmd

    def run(self) -> CommandResult:
        """Execute the command.

        Returns:
            Dict[str, DataClassJSONMixin | str]: Each key represents an MQTT topic and \
                the value represents the message that will be sent trough that topic

        """
        raise NotImplementedError

    def validate(self) -> None:
        """Validate the arguments (override it if custom logic is needed).

        This method should be invoked before executing the command

        Raises:
            ApiError:
            ParseError:

        """
