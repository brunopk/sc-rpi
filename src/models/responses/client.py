"""Contains `Client` class."""

from dataclasses import dataclass


@dataclass
class Client:
  """Represent a client of the API."""

  ip: str

  port: int
