"""Main class: `GetConfigResult`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi.commands.results import Result

if TYPE_CHECKING:
  from http import HTTPStatus

@dataclass
class Section:
    """Represents a section of leds in the strip."""

    end: int

    id: str

    name: str

    start: int

@dataclass
class StripConfig:
  """Contains configurations for the rpi_ws281x library."""

  brightness: int

  channel: int

  dma: int

  freq_hz: int

  invert: bool

  pin: int

  strip_length: int

  sections: list[Section]

@dataclass
class BrokerConfig:
  """Contains configurations for MQTT broker."""

  host: str

  port: int

@dataclass
class MQTTConfig:
  """Contains configurations for MQTT."""

  broker_config: BrokerConfig

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
        result_payload: GetConfigResultPayload,
    ) -> None:
        """Initialize the object.

        Args:
            status_code (HTTPStatus): Status code (same status codes used in HTTP).
            command_name (str): Name of the command that returned the response.
            result_payload (GetConfigResultPayload): The result of a command.

        """
        super().__init__(
            status_code,
            command_name,
            result_payload,
            None,
        )

