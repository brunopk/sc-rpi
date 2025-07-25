"""Contains the `Command` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, Optional, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from sc_rpi.config import Config
from sc_rpi.controllers import HardwareController
from sc_rpi.utils.config import load_configurations

if TYPE_CHECKING:
    from sc_rpi.models.responses import Response


CommandArgs = TypeVar("CommandArgs")

class Command(Generic[CommandArgs], DataClassJSONMixin):
    """Represents a command of SC RPi.

    To implement a command :

    1. Create the corresponding module in the `commands` package
    2. Create the main class for the command
        1. Re-implement the `run` method
        2. Re-implement `validate` method
    3. Create another class for command arguments


    Important considerations:
    - The command class must inherit from `Command`.
    - The command class must contain the `name` class attribute in order for the \
        Mashumaro discriminator to work correctly (discriminator is configured in the \
            `Config` class below).
    - The value for `name` should be the command name that API users will use when \
        invoking the command and it should be the snake-case version of the command \
            class.
    - `validate` method may be re-defined if custom logic is needed.
    - Command should not interact with MQTT, this is done by workers \
        (`src/sc_rpi/worker.py`).
    - In order to avoid multi-threading related issues with class attributes \
        (`hw_controller`, `config`, etc.), this class should be used only in one thread.
    - All subclasses must be imported before using them in order for mashumaro \
        discriminators to work correctly (even if only one of them is used).
    - If some error occurs when parsing from `dict` (`from_dict` method), Mashumaro \
        will raise `InvalidFieldValue`.

    """

    name: str

    args: CommandArgs

    _config: ClassVar[Optional[Config]] = None

    _hw_controller: ClassVar[Optional[HardwareController]] = None

    class Config(BaseConfig):
        """Mashumaro config."""

        discriminator = Discriminator(
            field="name",
            include_subtypes=True,
        )

    @classmethod
    def _load_hw_controller(cls, config: Config) -> HardwareController:
        if cls._hw_controller is None:
            print("_load_hw_controller invoked (REMOVE THIS print)")
            cls._hw_controller = HardwareController(config)
        return cls._hw_controller

    @classmethod
    def _load_sc_rpi_config(cls) -> Config:
        if cls._config is None:
            print("_load_sc_rpi_config invoked (REMOVE THIS print)")
            cls._config = load_configurations()
        return cls._config

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
    def __post_init__(self) -> None:
        """Post initialization (see Mashumaro documentation)."""
        self._config = self._load_sc_rpi_config()
        self._hw_controller = self._load_hw_controller(self._config)
