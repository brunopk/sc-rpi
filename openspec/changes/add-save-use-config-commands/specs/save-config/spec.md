# Spec Delta

## Purpose

Lets users persist the current strip configuration, including live section state, under a name so it can be restored later.

## ADDED Requirements

### Requirement: Save current configuration under a name
The system SHALL provide a `save_config` command with an optional `name`, an optional `description` (text) and an optional boolean `overwrite` (default `false`). It SHALL write the running configuration (the description and each section's range, color and on/off state) to `config/<name>.yaml`; the system appends `.yaml`, so it SHALL NOT be part of `name`. When `name` is omitted, the active configuration's name is used, exactly as if it had been given.

If a saved config with that name already exists, the command SHALL be rejected with `status` 409 and error code `CONFIG_ALREADY_EXISTS` and leave the file unchanged, unless `overwrite` is `true`, in which case it SHALL replace the file atomically (old or new complete content, never a partial one).

The command SHALL NOT change any section or re-render the strip.

On success the SC RPi result topic SHALL receive `status` 202, `command_name` `save_config` and a `payload` holding the saved configuration. The `payload` SHALL be the same as the `payload` of a `get_config` result for that configuration (the `Config` structure, not nested under another key), with secrets obfuscated as there.

#### Scenario: Save a new config
- **WHEN** a `save_config` command is received with `name` `party`
- **THEN** the current configuration is stored as `party` and the result has `status` 202, `command_name` `save_config`, and a `payload` holding the saved configuration, the same as a `get_config` result payload

#### Scenario: Name omitted with overwrite
- **WHEN** the active configuration is `night` and a `save_config` command is received without `name` and with `overwrite` `true`
- **THEN** `config/night.yaml` holds the running configuration, the result has `status` 202, and the active configuration is still `night`

#### Scenario: Name omitted without overwrite
- **WHEN** the active configuration is `night` and a `save_config` command is received without `name` and `overwrite` `false` or omitted
- **THEN** an error result with `status` 409 and code `CONFIG_ALREADY_EXISTS` is published and `night.yaml` is unchanged

#### Scenario: Name omitted while default is active
- **WHEN** the active configuration is `default` and a `save_config` command is received without `name`, with or without `overwrite`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published and `default.yaml` is unchanged

#### Scenario: Secrets hidden in the result
- **WHEN** a `save_config` command succeeds and the config contains secret values
- **THEN** every secret value in the result is an obfuscated placeholder and the real values appear nowhere in the result

#### Scenario: Secrets kept in the file
- **WHEN** a `save_config` command succeeds and the config contains secret values
- **THEN** the saved file holds the real values, so it remains a valid config

#### Scenario: Strip unchanged
- **WHEN** a `save_config` command succeeds
- **THEN** every section keeps its range, color and on/off state and the strip is not re-rendered

#### Scenario: Nothing changes on failure
- **WHEN** a `save_config` command fails for any reason
- **THEN** the running sections and the Home Assistant entities are unchanged and no file is written

#### Scenario: Name already exists
- **WHEN** a `save_config` command is received with a `name` that already has a saved config
- **THEN** an error result with `status` 409 and code `CONFIG_ALREADY_EXISTS` is published and the existing saved config is unchanged

#### Scenario: Overwrite an existing name
- **WHEN** a `save_config` command is received with a `name` that already has a saved config and `overwrite` `true`
- **THEN** the result has `status` 202 and the file now holds the current configuration

#### Scenario: Overwrite is atomic
- **WHEN** a `save_config` command with `overwrite` `true` replaces an existing saved config and the write is interrupted
- **THEN** the file holds either the complete old content or the complete new content, never a partial one

#### Scenario: Overwrite false is the default
- **WHEN** a `save_config` command is received with an existing `name` and `overwrite` `false` or omitted
- **THEN** an error result with `status` 409 and code `CONFIG_ALREADY_EXISTS` is published and the existing saved config is unchanged

#### Scenario: Section state round-trips
- **WHEN** a config is saved while a section is off with color `[0, 255, 0]` and later read back
- **THEN** that section is reported as off with color `[0, 255, 0]`

#### Scenario: Description saved
- **WHEN** a `save_config` command is received with `name` `party` and `description` `Friday lights`
- **THEN** the saved file and the result's saved configuration contain the description `Friday lights`

#### Scenario: Description omitted
- **WHEN** a `save_config` command is received without `description`
- **THEN** the command succeeds and the saved configuration has an empty description

### Requirement: Saved sections keep their ids and names
The `save_config` command SHALL save each section with the id and name it has in the running config, ordered by `start`. No Home Assistant entity is published or changed.

#### Scenario: Ids and names kept
- **WHEN** a `save_config` command is received with `name` `party` and the strip has two sections with ids `desk` and `shelf` and names `Desk` and `Shelf`
- **THEN** the saved sections have ids `desk` and `shelf` and names `Desk` and `Shelf`

#### Scenario: Home Assistant untouched
- **WHEN** a `save_config` command succeeds
- **THEN** no message is published to any Home Assistant topic

### Requirement: Reserved name `default`
The system SHALL reject `save_config` when the name used (the given `name`, or the active configuration's name when `name` is omitted) is `default`, with `status` 400 and error code `RESERVED_CONFIG_NAME`, and the initial config SHALL remain unchanged. The name `default` SHALL be compared case-insensitively, and the rejection SHALL apply even when `overwrite` is `true`.

#### Scenario: Save as default
- **WHEN** a `save_config` command is received with `name` `default`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published to the SC RPi result topic and no file is written

#### Scenario: Default in another letter case
- **WHEN** a `save_config` command is received with `name` `Default` or `DEFAULT`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published and no file is written (the reserved name is compared case-insensitively, as macOS and Windows file systems are case-insensitive)

#### Scenario: Default with overwrite
- **WHEN** a `save_config` command is received with `name` `default` and `overwrite` `true`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published and `default.yaml` is unchanged

### Requirement: Config names are names, not paths
The system SHALL accept only plain names for `name` (letters, digits, `-` and `_`) and SHALL reject any value that could refer to a location outside the `config/` directory, such as values containing path separators or `..`, with `status` 400 and error code `INVALID_CONFIG_NAME`.

#### Scenario: Path traversal attempt
- **WHEN** a `save_config` command is received with `name` `../secret`
- **THEN** an error result with `status` 400 and code `INVALID_CONFIG_NAME` is published and no file is written
