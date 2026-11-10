# Spec Delta

## Purpose

Lets users switch the running strip to a previously saved named configuration over MQTT without restarting the service.

## ADDED Requirements

### Requirement: Apply a saved configuration immediately
The system SHALL provide a `use_config` command with a required `name`. It SHALL load `config/<name>.yaml` and apply it immediately: rebuild the sections (ranges, colors, on/off state), replace the running description, re-render the strip and update the Home Assistant entities.

On success the loaded `name` becomes the active configuration, kept in memory only (`default` after a restart). On failure nothing changes, including the active configuration.

#### Scenario: Loaded config becomes active
- **WHEN** a `use_config` command with `name` `night` succeeds
- **THEN** a `status` command reports `night` as the active configuration

#### Scenario: Failed load keeps the active configuration
- **WHEN** the active configuration is `night` and a `use_config` command fails (for example `CONFIG_NOT_FOUND`)
- **THEN** the active configuration is still `night`

#### Scenario: Active configuration after restart
- **WHEN** the service restarts after a `use_config` command with `name` `night`
- **THEN** the active configuration is `default` and the strip is built from `config/default.yaml`

#### Scenario: Switch to a saved config
- **WHEN** a `use_config` command is received with `name` `night` and `night` exists
- **THEN** the strip shows the sections of `night` with their saved colors and on/off states, and Home Assistant state topics reflect them

#### Scenario: Description loaded
- **WHEN** a `use_config` command is received with `name` `party` and `party` has the description `Friday lights`
- **THEN** the running description becomes `Friday lights`

#### Scenario: Previous entities marked unavailable
- **WHEN** the running sections are `desk` and `shelf` and a `use_config` command loads `night`, which has `night_lamp`
- **THEN** the entities for `desk` and `shelf` are marked unavailable and not deleted, and the entity for `night_lamp` gets a discovery message (including its availability topic) and is marked available

#### Scenario: Result matches status
- **WHEN** a `use_config` command succeeds
- **THEN** the result has `status` 202 and `command_name` `use_config`, and its `payload` is identical to the `payload` of a `status` command received right after

### Requirement: No config files modified
The `use_config` command SHALL NOT create, modify or delete any config file; applying a config affects only the running state.

#### Scenario: No files changed
- **WHEN** a `use_config` command is executed
- **THEN** no file in `config/` is created, modified or deleted

### Requirement: Only strip sections are applied
The system SHALL NOT apply hardware-level strip settings or MQTT settings from the loaded config; only section definitions and state take effect.

#### Scenario: Saved config with different MQTT host
- **WHEN** a `use_config` command loads a config whose MQTT settings differ from the running ones
- **THEN** the running MQTT connection is unchanged

### Requirement: Invalid or unknown config names
The system SHALL leave the current strip state unchanged and publish an error result when: `name` is missing (`status` 400, code `MISSING_CONFIG_NAME`); the name is not a plain name of letters, digits, `-` and `_` (`status` 400, code `INVALID_CONFIG_NAME`); no saved config has that name (`status` 404, code `CONFIG_NOT_FOUND`); or the saved config exists but cannot be parsed or is invalid (`status` 500, code `INVALID_CONFIG`).

#### Scenario: Unknown name
- **WHEN** a `use_config` command is received with a `name` for which no saved config exists
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` is published and the strip is not modified

#### Scenario: Path traversal attempt
- **WHEN** a `use_config` command is received with `name` `../config`
- **THEN** an error result with `status` 400 and code `INVALID_CONFIG_NAME` is published and no file outside `config/` is read

#### Scenario: Unreadable saved config
- **WHEN** the saved config exists but is invalid
- **THEN** an error result with `status` 500 and code `INVALID_CONFIG` is published and the strip state is unchanged

#### Scenario: Sections do not fit the running strip
- **WHEN** a `use_config` command loads a config with a section whose `end` is not below the running strip length
- **THEN** an error result with `status` 500 and code `INVALID_CONFIG` is published and the strip state is unchanged
