# Spec Delta

## MODIFIED Requirements

### Requirement: Reset rebuilds sections from configuration
The `reset` command SHALL accept an optional `config_name`. When omitted, it SHALL load `config/default.yaml` and apply it exactly as `use_config` would. When present, it SHALL behave like `use_config` with that name, including the same validation and errors. Applying a config rebuilds the strip's sections from it (using each section's configured `color` and `is_on`), re-renders the strip, and publishes a successful status result listing the resulting sections to the result topic.

#### Scenario: Reset after edits
- **WHEN** sections have been edited or turned off and a `reset` command is received
- **THEN** the sections match the configured section definitions and a successful result is published

#### Scenario: Reset without a name
- **WHEN** a `reset` command is received without `config_name`
- **THEN** the strip state matches `config/default.yaml` and a successful result is published

#### Scenario: Reset with a saved config
- **WHEN** a `reset` command is received with `config_name` `party` and `party` exists
- **THEN** the strip state matches the `party` config

#### Scenario: Reset with an unknown name
- **WHEN** a `reset` command is received with a `config_name` that has no saved config
- **THEN** an error result is published and the strip state is unchanged

#### Scenario: Section configured off
- **WHEN** a loaded config has a section with `is_on` false
- **THEN** that section is off after loading

### Requirement: Reset updates Home Assistant entities
The `reset` command SHALL publish a state for every section to its Home Assistant state topic, using the section's color and the configured default section brightness, with an ON or OFF state matching the section's `is_on` value.

#### Scenario: Entities refreshed
- **WHEN** a `reset` command is received
- **THEN** each section's Home Assistant state topic receives a state matching the section's color and on/off state

#### Scenario: Section configured off
- **WHEN** a loaded config has a section with `is_on` false
- **THEN** its Home Assistant entity reports OFF
