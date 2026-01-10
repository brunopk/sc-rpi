"""Contains the `Invoker` enum."""

from enum import Enum


class Invoker(Enum):
  """Represents the invoker (who) of a command."""

  HOME_ASSISTANT = 1
  USER = 2
