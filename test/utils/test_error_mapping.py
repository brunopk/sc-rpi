"""Tests for `map_exception` with the configuration error codes."""

from http import HTTPStatus
from unittest import TestCase

import sc_rpi.commands  # noqa: F401 (must be imported first: avoids a circular import)
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.mappings import map_exception

EXPECTED_STATUS = {
    ErrorCode.MISSING_CONFIG_NAME: HTTPStatus.BAD_REQUEST,
    ErrorCode.INVALID_CONFIG_NAME: HTTPStatus.BAD_REQUEST,
    ErrorCode.RESERVED_CONFIG_NAME: HTTPStatus.BAD_REQUEST,
    ErrorCode.CONFIG_NOT_FOUND: HTTPStatus.NOT_FOUND,
    ErrorCode.CONFIG_ALREADY_EXISTS: HTTPStatus.CONFLICT,
    ErrorCode.INVALID_CONFIG: HTTPStatus.INTERNAL_SERVER_ERROR,
}


class TestErrorMapping(TestCase):
    """Tests for `map_exception`."""

    def test_config_error_codes(self) -> None:
        """Each configuration error code maps to the status given in the specs."""
        for code, status in EXPECTED_STATUS.items():
            with self.subTest(code=code):
                result = map_exception(ApiError(status, code), None)
                self.assertEqual(status.value, result.status)
                self.assertEqual(code, result.error.code)