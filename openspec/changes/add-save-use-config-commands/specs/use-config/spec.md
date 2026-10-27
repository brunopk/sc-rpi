# Spec Delta

## Purpose

Lets users switch the running strip to a previously saved named configuration over MQTT without restarting the service.

## ADDED Requirements

### Requirement: Apply a saved configuration immediately
The system SHALL provide a `use_config` command that requires a `config_name` argument, loads the saved config from `config/<config_name>.yaml`, and applies it immediately: sections are rebuilt from the config (ranges, colors, on/off state), the strip is re-rendered, and the Home Assistant entities are updated to match. A successful status result SHALL be published to the result topic, with `command_name` `use_config` and a `payload` listing the resulting sections (id, start, end, color, is_on). The result SHALL be identical to a `reset` result for the same `config_name`, except that `command_name` is `use_config`.

#### Scenario: Switch to a saved config
- **WHEN** a `use_config` command is received with `config_name` `night` and `night` exists
- **THEN** the strip shows the sections of `night` with their saved colors and on/off states, and Home Assistant state topics reflect them

#### Scenario: Same result as reset
- **WHEN** a `use_config` command and a `reset` command with the same `config_name` both succeed
- **THEN** their results are identical except for `command_name`

#### Scenario: Result lists the loaded sections
- **WHEN** a `use_config` command succeeds
- **THEN** the result has `status` 202, `command_name` `use_config`, and `payload.sections` with every loaded section's id, start, end, color and is_on

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
The system SHALL leave the current strip state unchanged and publish an error result when: `config_name` is missing (`status` 400, code `MISSING_CONFIG_NAME`); the name is not a plain name of letters, digits, `-` and `_` (`status` 400, code `INVALID_CONFIG_NAME`); no saved config has that name (`status` 404, code `CONFIG_NOT_FOUND`); or the saved config exists but cannot be parsed or is invalid (`status` 500, code `INVALID_CONFIG`).

#### Scenario: Unknown name
- **WHEN** a `use_config` command is received with a `config_name` for which no saved config exists
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` is published and the strip is not modified

#### Scenario: Path traversal attempt
- **WHEN** a `use_config` command is received with `config_name` `../config`
- **THEN** an error result with `status` 400 and code `INVALID_CONFIG_NAME` is published and no file outside `config/` is read

#### Scenario: Unreadable saved config
- **WHEN** the saved config exists but is invalid
- **THEN** an error result with `status` 500 and code `INVALID_CONFIG` is published and the strip state is unchanged
