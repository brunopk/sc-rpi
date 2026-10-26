# Spec Delta

## Purpose

Lets users switch the running strip to a previously saved named configuration over MQTT without restarting the service.

## ADDED Requirements

### Requirement: Apply a saved configuration immediately
The system SHALL provide a `use_config` command that requires a `config_name` argument, loads the saved config with that name, and applies it immediately: sections are rebuilt from the config (ranges, colors, on/off state), the strip is re-rendered, and the Home Assistant entities are updated to match. A successful result SHALL be published to the result topic.

#### Scenario: Switch to a saved config
- **WHEN** a `use_config` command is received with `config_name` `night` and `night` exists
- **THEN** the strip shows the sections of `night` with their saved colors and on/off states, and Home Assistant state topics reflect them

### Requirement: Applied config is not persisted
The system SHALL NOT change which config is loaded at startup as a result of `use_config`; on restart the system SHALL load `config/default.yaml`.

#### Scenario: Restart after use_config
- **WHEN** `use_config` was executed with `night` and the service is then restarted
- **THEN** the strip is initialized from `config/default.yaml`

### Requirement: Only strip sections are applied
The system SHALL NOT apply hardware-level strip settings or MQTT settings from the loaded config; only section definitions and state take effect.

#### Scenario: Saved config with different MQTT host
- **WHEN** a `use_config` command loads a config whose MQTT settings differ from the running ones
- **THEN** the running MQTT connection is unchanged

### Requirement: Invalid or unknown config names
The system SHALL reject a missing `config_name`, a name that is not a plain name (letters, digits, `-`, `_`), and a name with no saved config, publishing an error result and leaving the current strip state unchanged.

#### Scenario: Unknown name
- **WHEN** a `use_config` command is received with a `config_name` for which no saved config exists
- **THEN** an error result is published and the strip is not modified

#### Scenario: Path traversal attempt
- **WHEN** a `use_config` command is received with `config_name` `../config`
- **THEN** an error result is published and no file outside `config/` is read

#### Scenario: Unreadable saved config
- **WHEN** the saved config exists but is invalid
- **THEN** an error result is published and the strip state is unchanged
