# Spec Delta

## Purpose

Lets users persist the current strip configuration, including live section state, under a name so it can be restored later.

## ADDED Requirements

### Requirement: Save current configuration under a name
The system SHALL provide a `save_config` command that requires a `name` argument and accepts an optional `description` (text), and writes the current in-memory configuration, including the description and each section's range, color and on/off state, to the file `config/<name>.yaml` (the `.yaml` extension is appended by the system and SHALL NOT be part of `name`). If a saved config with that name already exists, the command SHALL be rejected with `status` 409 and error code `CONFIG_ALREADY_EXISTS`, and the existing file SHALL remain unchanged. The command SHALL NOT change any section's range, color or on/off state, and SHALL NOT re-render the strip. On success the result published to the SC RPi result topic SHALL have `status` 202, `command_name` `save_config`, and a `payload` with the saved `name` and, under `config`, the saved configuration. The saved configuration in the result SHALL have the same structure as a `get_config` result payload, with secret values obfuscated exactly as in a `get_config` result (the real values SHALL NOT appear in the result).

Example result payload shape: `{"name": "party", "config": {...}}`.

#### Scenario: Save a new config
- **WHEN** a `save_config` command is received with `name` `party`
- **THEN** the current configuration is stored as `party` and the result has `status` 202, `command_name` `save_config`, `payload.name` `party`, and `payload.config` holding the saved configuration in the same structure as a `get_config` result payload

#### Scenario: Secrets hidden
- **WHEN** a `save_config` command succeeds and the config contains an MQTT password
- **THEN** the result's MQTT password is an obfuscated placeholder, not the real value

#### Scenario: Strip unchanged
- **WHEN** a `save_config` command succeeds
- **THEN** every section keeps its range, color and on/off state and the strip is not re-rendered

#### Scenario: Nothing changes on failure
- **WHEN** a `save_config` command fails for any reason
- **THEN** the running sections and the Home Assistant entities are unchanged and no file is written

#### Scenario: Name already exists
- **WHEN** a `save_config` command is received with a `name` that already has a saved config
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
The system SHALL reject `save_config` when `name` is `default` with `status` 400 and error code `RESERVED_CONFIG_NAME`, and the initial config SHALL remain unchanged. The name `default` SHALL be compared case-insensitively.

#### Scenario: Save as default
- **WHEN** a `save_config` command is received with `name` `default`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published to the SC RPi result topic and no file is written

#### Scenario: Default in another letter case
- **WHEN** a `save_config` command is received with `name` `Default` or `DEFAULT`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published and no file is written (the reserved name is compared case-insensitively, as macOS and Windows file systems are case-insensitive)

### Requirement: Config names are names, not paths
The system SHALL accept only plain names for `name` (letters, digits, `-` and `_`) and SHALL reject any value that could refer to a location outside the `config/` directory, such as values containing path separators or `..`, with `status` 400 and error code `INVALID_CONFIG_NAME`. A missing `name` SHALL be rejected with `status` 400 and error code `MISSING_CONFIG_NAME`.

#### Scenario: Path traversal attempt
- **WHEN** a `save_config` command is received with `name` `../secret`
- **THEN** an error result with `status` 400 and code `INVALID_CONFIG_NAME` is published and no file is written

#### Scenario: Missing name
- **WHEN** a `save_config` command is received without `name`
- **THEN** an error result with `status` 400 and code `MISSING_CONFIG_NAME` is published and no file is written
