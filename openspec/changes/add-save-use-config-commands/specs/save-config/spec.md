# Spec Delta

## Purpose

Lets users persist the current strip configuration, including live section state, under a name so it can be restored later.

## ADDED Requirements

### Requirement: Save current configuration under a name
The system SHALL provide a `save_config` command that requires a `config_name` argument and writes the current in-memory configuration, including each section's range, color and on/off state, to the saved config identified by that name in the `config/` directory. An existing saved config with the same name SHALL be overwritten.

#### Scenario: Save a new config
- **WHEN** a `save_config` command is received with `config_name` `party`
- **THEN** the current configuration is stored as `party` and a successful result is published to the result topic

#### Scenario: Overwrite an existing config
- **WHEN** a `save_config` command is received with a `config_name` that already exists, other than `default`
- **THEN** the saved config is replaced with the current configuration

#### Scenario: Section state round-trips
- **WHEN** a config is saved while a section is off with color `[0, 255, 0]` and later read back
- **THEN** that section is reported as off with color `[0, 255, 0]`

### Requirement: Reserved name `default`
The system SHALL reject `save_config` when `config_name` is `default`, and the boot config SHALL remain unchanged.

#### Scenario: Save as default
- **WHEN** a `save_config` command is received with `config_name` `default`
- **THEN** an error result is published to the result topic and no file is written

### Requirement: Config names are names, not paths
The system SHALL accept only plain names for `config_name` (letters, digits, `-` and `_`) and SHALL reject any value that could refer to a location outside the `config/` directory, such as values containing path separators or `..`. A missing `config_name` SHALL be rejected.

#### Scenario: Path traversal attempt
- **WHEN** a `save_config` command is received with `config_name` `../secret`
- **THEN** an error result is published and no file is written

#### Scenario: Missing name
- **WHEN** a `save_config` command is received without `config_name`
- **THEN** an error result is published and no file is written
