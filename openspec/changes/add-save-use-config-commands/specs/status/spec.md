# Spec Delta

## ADDED Requirements

### Requirement: Status reports the active configuration and description
The `status` command result `payload` SHALL include `active_configuration`: the name of the configuration that `reset` without `name` reloads. It is `default` after startup, and `use_config` and `reset` with a `name` change it. The `payload` SHALL also include the running `description` (empty when the loaded config has none), and SHALL still list the running sections (id, start, end, color, is_on).

#### Scenario: Description after use_config
- **WHEN** a `use_config` command loads a config with the description `Friday lights` and a `status` command is then received
- **THEN** `payload.description` is `Friday lights`

#### Scenario: Description at startup
- **WHEN** a `status` command is received and the initial configuration has no description
- **THEN** `payload.description` is an empty string

#### Scenario: Active configuration at startup
- **WHEN** a `status` command is received and no config has been loaded since startup
- **THEN** `payload.active_configuration` is `default`

#### Scenario: Active configuration after use_config
- **WHEN** a `use_config` command with `name` `night` succeeds and a `status` command is then received
- **THEN** `payload.active_configuration` is `night` and `payload.sections` lists the running sections

#### Scenario: Saving does not change the active configuration
- **WHEN** the active configuration is `night` and a `save_config` command with `name` `party` succeeds
- **THEN** a `status` command reports `night` as the active configuration
