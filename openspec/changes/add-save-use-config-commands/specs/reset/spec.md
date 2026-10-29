# Spec Delta

## MODIFIED Requirements

### Requirement: Reset rebuilds sections from configuration
The `reset` command SHALL accept an optional `config_name`. When omitted, it SHALL load `config/default.yaml` and apply it exactly as `use_config` would. When present, it SHALL behave like `use_config` with that name, including the same validation and errors. Applying a config rebuilds the strip's sections from it (using each section's configured `color` and `is_on`), re-renders the strip, and publishes a successful status result listing the resulting sections to the SC RPi result topic.

#### Scenario: Reset after edits
- **WHEN** sections have been edited or turned off and a `reset` command is received
- **THEN** the sections match the configured section definitions and the result has `status` 202, `command_name` `reset`, and `payload.sections` listing those sections

#### Scenario: Reset without a name
- **WHEN** a `reset` command is received without `config_name`
- **THEN** the strip state matches `config/default.yaml` and the result has `status` 202, `command_name` `reset`, and `payload.sections` listing those sections

#### Scenario: Reset with a saved config
- **WHEN** a `reset` command is received with `config_name` `party` and `party` exists
- **THEN** the strip state matches the `party` config

#### Scenario: Reset with an unknown name
- **WHEN** a `reset` command is received with a `config_name` that has no saved config
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` is published and the strip state is unchanged

#### Scenario: Section configured off
- **WHEN** a loaded config has a section with `is_on` false
- **THEN** that section is off after loading

### Requirement: Reset updates Home Assistant entities
The Home Assistant discovery message of every section SHALL include an availability topic. The `reset` command SHALL mark unavailable (publish `offline` to the availability topic, without deleting the entity) the current Home Assistant entities, SHALL publish a discovery message (including the availability topic) for every loaded section, SHALL mark the loaded sections' entities available, and SHALL publish a state for every loaded section to its Home Assistant state topic, using the section's color and the configured default section brightness, with an ON or OFF state matching the section's `is_on` value.

#### Scenario: Entities refreshed
- **WHEN** a `reset` command is received
- **THEN** each loaded section's discovery message (including its availability topic) is published, and each section's Home Assistant state topic receives a state matching the section's color and on/off state

#### Scenario: Section configured off
- **WHEN** a loaded config has a section with `is_on` false
- **THEN** its Home Assistant entity reports OFF

#### Scenario: Previous entities unpublished
- **WHEN** the running sections are `party_section_1` and `party_section_2` and a `reset` command without `config_name` loads a default config with `section_1`
- **THEN** the entities for the `party_` sections are marked unavailable and not deleted, and the entity for `section_1` is published and marked available
