# Spec Delta

## ADDED Requirements

### Requirement: Get a saved configuration
The `get_config` command SHALL require a `name` and return the contents of that saved config without applying it or changing the strip. Name validation and errors (`MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME`, `CONFIG_NOT_FOUND`, `INVALID_CONFIG`) SHALL match `use_config`.

#### Scenario: Read a saved config
- **WHEN** a `get_config` command is received with `name` `party` and `party` exists
- **THEN** the result payload contains the `party` configuration (general settings, strip settings, the `description`, and each section's id, name, start, end, `color` and `is_on`) and the strip is unchanged

#### Scenario: Read back after save
- **WHEN** a `save_config` command with `name` `X` succeeds and a `get_config` command with `name` `X` is then received
- **THEN** the `get_config` result payload equals the `save_config` result payload

#### Scenario: Description returned
- **WHEN** a `get_config` command is received with `name` `party` and `party` was saved with the description `Friday lights`
- **THEN** the result contains the description `Friday lights`

#### Scenario: Missing name
- **WHEN** a `get_config` command is received without `name`
- **THEN** an error result with `status` 400 and code `MISSING_CONFIG_NAME` is published

#### Scenario: Unknown name
- **WHEN** a `get_config` command is received with a `name` that has no saved config
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` is published

### Requirement: No config files modified
The `get_config` command SHALL NOT create, modify or delete any config file; it only reads the saved config named by `name`.

#### Scenario: No files changed
- **WHEN** a `get_config` command is executed
- **THEN** no file in `config/` is created, modified or deleted

## MODIFIED Requirements

### Requirement: MQTT settings in result
Any `get_config` result SHALL have the structure of a saved configuration file (the `Config` model). Every configuration value classified as secret SHALL be replaced by an obfuscated placeholder, and the real values SHALL NOT appear in the result. All other values SHALL be returned as they are. The set of secret values is defined in one place in the code; the MQTT password is currently the only one.

#### Scenario: Broker settings
- **WHEN** a `get_config` command is executed
- **THEN** the result contains the MQTT broker host and port under `mqtt.broker`

#### Scenario: Secrets hidden, other values returned
- **WHEN** a `get_config` command is executed and the saved config contains secret values
- **THEN** every secret value in the result is an obfuscated placeholder, the real values appear nowhere in the result, and every other configuration value is returned as it is in the saved config

## REMOVED Requirements

### Requirement: Return running configuration
**Reason**: `get_config` now reads saved configurations only. The running state is reported by `status`, and `save_config` returns the running configuration it saves.
**Migration**: Use `status` to read the live sections. To get the full running configuration, send `save_config` with a name. To read a saved config, send `get_config` with its `name`.