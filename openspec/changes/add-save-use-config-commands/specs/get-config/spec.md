# Spec Delta

## ADDED Requirements

### Requirement: Get a saved configuration
The `get_config` command SHALL accept an optional `config_name` and, when present, return that saved config's contents without loading it or changing the strip. Name validation and unknown-name errors SHALL match `use_config`.

#### Scenario: Read a saved config
- **WHEN** a `get_config` command is received with `config_name` `party` and `party` exists
- **THEN** the result payload contains the `party` configuration and the strip is unchanged

#### Scenario: Unknown name
- **WHEN** a `get_config` command is received with a `config_name` that has no saved config
- **THEN** an error result is published

## MODIFIED Requirements

### Requirement: Return running configuration
The `get_config` command SHALL, when `config_name` is omitted, return the running configuration (general settings, strip settings, and each section's id, name, start, end, `color` and `is_on`) in a successful result on the result topic, without changing the strip.

#### Scenario: Get configuration
- **WHEN** a `get_config` command is received without `config_name`
- **THEN** a successful result containing the running configuration, with `color` and `is_on` for every section, is published

### Requirement: MQTT settings in result
Any `get_config` result SHALL include the MQTT broker host and port and the password obfuscated; no other MQTT credentials SHALL be included. The real password SHALL NOT appear in the result.

#### Scenario: Broker settings
- **WHEN** a `get_config` command is executed
- **THEN** the result contains the broker host and port

#### Scenario: Password hidden
- **WHEN** a `get_config` command is executed and the config contains an MQTT password
- **THEN** the result's MQTT password is an obfuscated placeholder, not the real value
