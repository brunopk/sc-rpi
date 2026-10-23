"""Contains the `Invoker` enum."""

from enum import Enum


class Invoker(Enum):
  """Represents the invoker (who or what) of a command.

  Now is not being used, in the future it can be returned in the result topic.
  """

  HOME_ASSISTANT = 1
  USER = 2
