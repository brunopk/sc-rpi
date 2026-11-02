# Spec Delta

## ADDED Requirements

### Requirement: Get a saved configuration
The `get_config` command SHALL accept an optional `name` and, when present, return that saved config's contents without applying it or changing the strip. Name validation and errors (`INVALID_CONFIG_NAME`, `CONFIG_NOT_FOUND`, `INVALID_CONFIG`) SHALL match `use_config`.

#### Scenario: Read a saved config
- **WHEN** a `get_config` command is received with `name` `party` and `party` exists
- **THEN** the result payload contains the `party` configuration and the strip is unchanged

#### Scenario: Read back after save
- **WHEN** a `save_config` command with `name` `X` succeeds and a `get_config` command with `name` `X` is then received
- **THEN** the `get_config` result contains the same configuration that was saved, matching the `save_config` result payload's configuration

#### Scenario: Description returned
- **WHEN** a `get_config` command is received with `name` `party` and `party` was saved with the description `Friday lights`
- **THEN** the result contains the description `Friday lights`

#### Scenario: Unknown name
- **WHEN** a `get_config` command is received with a `name` that has no saved config
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` is published

## MODIFIED Requirements

### Requirement: Return running configuration
The `get_config` command SHALL, when `name` is omitted, return the running configuration (general settings, strip settings, the `description`, and each section's id, name, start, end, `color` and `is_on`) in a successful result on the SC RPi result topic, without changing the strip.

#### Scenario: Get configuration
- **WHEN** a `get_config` command is received without `name`
- **THEN** a successful result containing the running configuration, with `color` and `is_on` for every section, is published

### Requirement: MQTT settings in result
Any `get_config` result SHALL have the structure of a saved configuration file (the `Config` model). Secret configuration values (currently the MQTT password) SHALL be replaced by an obfuscated placeholder, and the real values SHALL NOT appear in the result. All other values SHALL be returned as they are.

#### Scenario: Broker settings
- **WHEN** a `get_config` command is executed
- **THEN** the result contains the MQTT broker host and port

#### Scenario: Non-secret values returned
- **WHEN** a `get_config` command is executed
- **THEN** the result contains every configuration value as it is in the config, except secret values

#### Scenario: Secrets hidden
- **WHEN** a `get_config` command is executed and the config contains an MQTT password
- **THEN** the result's MQTT password is an obfuscated placeholder, not the real value
