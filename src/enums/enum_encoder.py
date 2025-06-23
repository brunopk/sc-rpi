"""Contains the EnumEncoder class."""

from enum import Enum
from json import JSONEncoder


class EnumEncoder(JSONEncoder):
    """Used to encode enums as strings."""

    def default(self, obj: object) -> str:
      """Convert a enum instance to a string.

      Args:
          obj (_type_): Object to be converted

      Returns:
          _type_: The string representation of the enum instance.

      """
      if isinstance(obj, Enum):
        return obj.name
      return super().default(obj)
