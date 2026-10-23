"""Main class: `GetConfigResult`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.get_config.result.mqtt import MQTTConfig
from sc_rpi.commands.get_config.result.strip import StripConfig
from sc_rpi.commands.results import Result

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class GetConfigResultPayload(DataClassJSONMixin):
  """Main configuration class.

  This class may encapsulate other configuration classes.
  """

  connection_timeout: float

  default_gateway: str

  default_network_interface: str

  env: str

  log_level: str

  mqtt_config: MQTTConfig

  status_led: int

  strip_config: StripConfig

@dataclass
class GetConfigResult(Result[GetConfigResultPayload]):
    """Contains available sections."""

    payload: GetConfigResultPayload

    def __init__(
        self,
        status_code: HTTPStatus,
        command_name: str,
        payload: GetConfigResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            payload (HelpResultPayload): The result of the command.

        """
        super().__init__(
            status_code,
            command_name,
            payload,
            None,
        )
