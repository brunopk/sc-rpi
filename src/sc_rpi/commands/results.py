"""Contain the result classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

if TYPE_CHECKING:
    from http import HTTPStatus

    from sc_rpi.enums.error_code import ErrorCode
    from sc_rpi.models.color import Color

ResultPayload = TypeVar("ResultPayload")

@dataclass
class Error:
    """Contains the error code which indicates what is the error \

    about and a description for more information (optional).
    """

    code: ErrorCode

    description: str

@dataclass
class Section:
    """Represents a section of leds in the strip."""

    id: str

    start: int

    end: int

    color: Color

    is_on: bool

@dataclass
class Result(Generic[ResultPayload], DataClassJSONMixin):
    """Response for all commands.

    It may be an error or a successful response.
    """

    status: int

    command_name: Optional[str]

    payload: Optional[ResultPayload]

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
            payload (Payload | None, optional): The result of a command. Defaults to \
                None.
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

        omit_none = True
        discriminator = Discriminator(
            field="command_name",
            include_subtypes=True,
        )

@dataclass
class StatusResultPayload(DataClassJSONMixin):
  """Contains available sections."""

  sections: list[Section]

@dataclass
class StatusResult(Result[StatusResultPayload]):
    """Contains available sections."""

    payload: StatusResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: StatusResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (StatusPayload): Payload for the result.

        """
        super().__init__(status_code, command_name, payload, None)
