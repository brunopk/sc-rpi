"""Successful response for all commands."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from sc_rpi.models import Error

if TYPE_CHECKING:
    from http import HTTPStatus

Payload = TypeVar("Payload")

@dataclass
class Response(Generic[Payload], DataClassJSONMixin):
    """Response for all commands.

    It may be an error or a successful response.
    """

    status: int

    command_name: Optional[str]

    payload: Optional[Payload]

    error: Optional[Error]

    def __init__(
        self,
        status: HTTPStatus,
        command_name: str,
        payload: Optional[Payload] = None,
        error: Optional[Error] = None,
    ) -> None:
        """Initialize the object.

        Args:
            status (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (Any | None, optional): The result of a command. Defaults to None.
            error (Error | None, optional): Error object. Use it only if the command \
                failed (`payload` and `error` cannot be set at the same time). \
                    Defaults to None.

        """
        self.status = status.value
        self.payload = payload
        self.error = error
        self.command_name = command_name

    class Config(BaseConfig):
        """Mashumaro config."""

        discriminator = Discriminator(
            field="command_name",
            include_subtypes=True,
        )
