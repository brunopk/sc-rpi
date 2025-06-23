"""Represent a parsing error when parsing from JSON."""
from __future__ import annotations

from http import HTTPStatus

from jsonschema import ValidationError

from enums import ErrorCode

from .api_error import ApiError


class ParseError(ApiError):
    """Represent a parsing error when parsing from JSON."""

    def __init__(self, errors: list[ValidationError] | list[str]) -> None:
      """Initialize the object.

      Args:
          errors (list[ValidationError] | list[str]): list of accumulated errors

      """
      super().__init__(HTTPStatus.BAD_REQUEST, ErrorCode.PARSE_ERROR)
      aux1 = [
          f"error in {self.__get_path__(e)} : {e.message}"
          for e in errors
          if isinstance(e, ValidationError)
      ]
      aux2 = [e for e in errors if isinstance(e, str)]
      self.message = str(aux1) if len(aux1) > 0 else str(aux2)

    def __get_path__(self, error: ValidationError) -> str:
        """Obtain the path of the key that generates the error."""
        result = "args"
        for e in error.absolute_path:
            if isinstance(e, int):
                result += f"[{e}]"
            else:
                result += f".{e}"
        return result
