"""Successful response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from sc_rpi.models.command.command_result.sc_rpi_error import ScRpiError

if TYPE_CHECKING:
    from http import HTTPStatus

ScRpiResultPayload = TypeVar("ScRpiResultPayload")

@dataclass
class ScRpiResult(Generic[ScRpiResultPayload], DataClassJSONMixin):
    """Response for all commands.

    It may be an error or a successful response.
    """

    status: int

    command_name: Optional[str]

    payload: Optional[ScRpiResultPayload]

    error: Optional[ScRpiError]

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        sc_rpi_result_payload: Optional[ScRpiResultPayload] = None,
        sc_rpi_error: Optional[ScRpiError] = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            sc_rpi_result_payload (Any | None, optional): The result of a command. \
                Defaults to None.
            sc_rpi_error (Error | None, optional): Error object. Use it only if the \
                command failed (`payload` and `error` cannot be set at the same time). \
                    Defaults to None.

        """
        self.status = status.value
        self.payload = sc_rpi_result_payload
        self.error = sc_rpi_error
        self.command_name = command_name

    class Config(BaseConfig):
        """Mashumaro config."""

        discriminator = Discriminator(
            field="command_name",
            include_subtypes=True,
        )
