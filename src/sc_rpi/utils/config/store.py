"""Named configuration store: names, paths and file I/O for `config/<name>.yaml`.

All name-to-path handling lives here, so no command builds a file path itself.
"""

from __future__ import annotations

import contextlib
import os
import re
import tempfile
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.errors.api_error import ApiError
from sc_rpi.utils.config.main import load_configurations

if TYPE_CHECKING:
    from sc_rpi.config import Config

CONFIG_DIR = Path("config")
"""Directory with all configs, resolved from the current working directory."""

DEFAULT_NAME = "default"
"""Name of the initial config (`config/default.yaml`)."""

_NAME_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,64}")


def validate_name(name: object) -> str:
    """Check that `name` is a plain config name.

    Only letters, digits, `-` and `_` are accepted (1 to 64 characters), so no path
    separator, dot or `..` can reach the filesystem.

    Raises:
        ApiError: `MISSING_CONFIG_NAME` (400) if `name` is missing or empty,
            `INVALID_CONFIG_NAME` (400) if it is not a valid name.

    Returns:
        str: The validated name.

    """
    if name is None or name == "":
        raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.MISSING_CONFIG_NAME)
    if not isinstance(name, str) or _NAME_PATTERN.fullmatch(name) is None:
        raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.INVALID_CONFIG_NAME)
    return name


def path_for(name: str) -> Path:
    """Return the file path of the config `name` (the name is validated)."""
    return CONFIG_DIR / f"{validate_name(name)}.yaml"


def load(name: str) -> Config:
    """Load the saved config `name`.

    Raises:
        ApiError: `CONFIG_NOT_FOUND` (404) if there is no such config,
            `INVALID_CONFIG` (500) if the file cannot be parsed, plus the errors of
            `validate_name`.

    """
    path = path_for(name)
    if not path.is_file():
        raise ApiError(HTTPStatus.NOT_FOUND, ErrorCode.CONFIG_NOT_FOUND)
    return load_configurations(path)


def save(name: str, config: Config) -> None:
    """Save `config` as `config/<name>.yaml` without ever overwriting a file.

    The YAML is written to a temporary file (mode `0600`, as it holds credentials),
    which is then given its final name with `os.link`. Unlike `os.rename`, `os.link`
    fails if the target exists, so there is no check-then-write race and a crash
    mid-write never leaves a half-written config under a real name.

    Raises:
        ApiError: `RESERVED_CONFIG_NAME` (400) for `default` (case-insensitive),
            `CONFIG_ALREADY_EXISTS` (409) if the name is taken, plus the errors of
            `validate_name`.

    """
    target = path_for(name)
    if name.lower() == DEFAULT_NAME:
        raise ApiError(HTTPStatus.BAD_REQUEST, ErrorCode.RESERVED_CONFIG_NAME)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # mkstemp creates the file with mode 0600.
    fd, tmp_name = tempfile.mkstemp(dir=CONFIG_DIR, prefix=".tmp-", suffix=".yaml")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump(config.to_dict(), f, sort_keys=False)
        try:
            os.link(tmp, target)
        except FileExistsError as ex:
            raise ApiError(HTTPStatus.CONFLICT, ErrorCode.CONFIG_ALREADY_EXISTS) from ex
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()
