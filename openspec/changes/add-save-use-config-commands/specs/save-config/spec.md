# Spec Delta

## Purpose

Lets users persist the current strip configuration, including live section state, under a name so it can be restored later.

## ADDED Requirements

### Requirement: Save current configuration under a name
The system SHALL provide a `save_config` command that requires a `config_name` argument and writes the current in-memory configuration, including each section's range, color and on/off state, to the file `config/<config_name>.yaml` (the `.yaml` extension is appended by the system and SHALL NOT be part of `config_name`). If a saved config with that name already exists, the command SHALL be rejected with `status` 409 and error code `CONFIG_ALREADY_EXISTS`, and the existing file SHALL remain unchanged. The command SHALL NOT change any section's range, color or on/off state, and SHALL NOT re-render the strip. On success the result published to the result topic SHALL have `status` 202, `command_name` `save_config`, and a `payload` containing the saved `config_name` and the saved configuration in the same structure a `get_config` result returns, including the obfuscated MQTT password (the real password SHALL NOT appear in the result).

#### Scenario: Save a new config
- **WHEN** a `save_config` command is received with `config_name` `party`
- **THEN** the current configuration is stored as `party` and the result has `status` 202, `command_name` `save_config`, `payload.config_name` `party`, and the saved configuration in the same structure as a `get_config` result

#### Scenario: Password hidden
- **WHEN** a `save_config` command succeeds and the config contains an MQTT password
- **THEN** the result's MQTT password is an obfuscated placeholder, not the real value

#### Scenario: Strip unchanged
- **WHEN** a `save_config` command succeeds
- **THEN** every section keeps its range, color and on/off state and the strip is not re-rendered

#### Scenario: Nothing changes on failure
- **WHEN** a `save_config` command fails for any reason
- **THEN** the running sections and the Home Assistant entities are unchanged and no file is written

#### Scenario: Name already exists
- **WHEN** a `save_config` command is received with a `config_name` that already has a saved config
- **THEN** an error result with `status` 409 and code `CONFIG_ALREADY_EXISTS` is published and the existing saved config is unchanged

#### Scenario: Section state round-trips
- **WHEN** a config is saved while a section is off with color `[0, 255, 0]` and later read back
- **THEN** that section is reported as off with color `[0, 255, 0]`

### Requirement: Saved sections get config-specific ids
The `save_config` command SHALL give each section, ordered by `start`, the id `<config_name>_section_<n>`, where `n` is the section's 1-based position. Section names SHALL be kept as they are. These generated ids SHALL be written to the saved file and SHALL replace the ids of the running sections, so the running strip matches the saved config. Home Assistant SHALL then be updated: the current entities are marked unavailable (published `offline` to their availability topic, not deleted) and entities for the new ids are published with each section's current color and on/off state and marked available.

#### Scenario: Ids are prefixed and names kept
- **WHEN** a `save_config` command is received with `config_name` `party` and the strip has two sections named `Desk` and `Shelf`
- **THEN** the saved sections have ids `party_section_1` and `party_section_2` and names `Desk` and `Shelf`

#### Scenario: Running sections adopt the new ids
- **WHEN** a `save_config` command with `config_name` `party` succeeds
- **THEN** the running sections have the ids `party_section_1`, `party_section_2`, ..., and a `get_config` without `config_name` returns the same sections as the `save_config` result

#### Scenario: Home Assistant entities replaced
- **WHEN** a `save_config` command with `config_name` `party` succeeds and the running sections were `section_1` and `section_2`
- **THEN** the entities for `section_1` and `section_2` are marked unavailable and not deleted, and the entities for `party_section_1` and `party_section_2` are published with the sections' current color and on/off state and marked available

#### Scenario: Saving again under another name
- **WHEN** the running sections are `party_section_1` and `party_section_2` and a `save_config` command with `config_name` `night` succeeds
- **THEN** the saved and running section ids are `night_section_1` and `night_section_2`, with no `party_` prefix

### Requirement: Reserved name `default`
The system SHALL reject `save_config` when `config_name` is `default` with `status` 400 and error code `RESERVED_CONFIG_NAME`, and the boot config SHALL remain unchanged.

#### Scenario: Save as default
- **WHEN** a `save_config` command is received with `config_name` `default`
- **THEN** an error result with `status` 400 and code `RESERVED_CONFIG_NAME` is published to the result topic and no file is written

### Requirement: Config names are names, not paths
The system SHALL accept only plain names for `config_name` (letters, digits, `-` and `_`) and SHALL reject any value that could refer to a location outside the `config/` directory, such as values containing path separators or `..`, with `status` 400 and error code `INVALID_CONFIG_NAME`. A missing `config_name` SHALL be rejected with `status` 400 and error code `MISSING_CONFIG_NAME`.

#### Scenario: Path traversal attempt
- **WHEN** a `save_config` command is received with `config_name` `../secret`
- **THEN** an error result with `status` 400 and code `INVALID_CONFIG_NAME` is published and no file is written

#### Scenario: Missing name
- **WHEN** a `save_config` command is received without `config_name`
- **THEN** an error result with `status` 400 and code `MISSING_CONFIG_NAME` is published and no file is written
