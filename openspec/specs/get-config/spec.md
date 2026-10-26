# get-config Specification

## Purpose

Lets users inspect the running configuration of SC RPi over MQTT.

## Requirements

### Requirement: Return running configuration
The `get_config` command SHALL return the running configuration (general settings, strip settings, and each section's id, name, start and end) in a successful result on the result topic, without changing the strip.

#### Scenario: Get configuration
- **WHEN** a `get_config` command is received
- **THEN** a successful result containing the running configuration is published

### Requirement: MQTT settings in result
The `get_config` result SHALL include the MQTT broker host and port and SHALL NOT include MQTT credentials.

#### Scenario: Broker settings
- **WHEN** a `get_config` command is executed
- **THEN** the result contains the broker host and port and no username or password
