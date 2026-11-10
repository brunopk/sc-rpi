# Spec Delta

## MODIFIED Requirements

### Requirement: Reset rebuilds sections from configuration
The `reset` command SHALL accept an optional `name`. When omitted, it SHALL load the active configuration (`config/<active>.yaml`, which is `config/default.yaml` until a config has been loaded) and apply it exactly as `use_config` would. When present, it SHALL behave like `use_config` with that name, including the same validation and errors, and that name becomes the active configuration. Applying a config rebuilds the strip's sections from it (using each section's configured `color` and `is_on`), re-renders the strip, and publishes a successful status result listing the resulting sections to the SC RPi result topic.

#### Scenario: Reset after edits
- **WHEN** sections have been edited or turned off and a `reset` command is received
- **THEN** the sections match the active configuration's section definitions

#### Scenario: Reset without a name at startup
- **WHEN** no config has been loaded since startup and a `reset` command is received without `name`
- **THEN** the strip state matches `config/default.yaml`

#### Scenario: Result matches status
- **WHEN** a `reset` command succeeds, with or without `name`
- **THEN** the result has `status` 202 and `command_name` `reset`, and its `payload` is identical to the `payload` of a `status` command received right after

#### Scenario: Reset restores the active configuration
- **WHEN** a `use_config` command with `name` `night` succeeded, sections were then edited, and a `reset` command is received without `name`
- **THEN** the strip state matches the `night` config, not `config/default.yaml`

#### Scenario: Reset with a saved config
- **WHEN** a `reset` command is received with `name` `party` and `party` exists
- **THEN** the strip state matches the `party` config and `party` is the active configuration

#### Scenario: Named reset changes the active configuration
- **WHEN** a `reset` command with `name` `party` succeeds and a `reset` command without `name` is then received
- **THEN** the strip state matches the `party` config

#### Scenario: Active configuration file unavailable
- **WHEN** the active configuration's file no longer exists or is invalid and a `reset` command is received without `name`
- **THEN** an error result with `status` 404 and code `CONFIG_NOT_FOUND` (or `status` 500 and code `INVALID_CONFIG`) is published, the strip state is unchanged and the active configuration is unchanged

#### Scenario: Reset with an unknown name
- **WHEN** a `reset` command is received with a `name` that has no saved config
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

#### Scenario: Previous entities marked unavailable
- **WHEN** the running sections are `desk` and `shelf` and a `reset` command without `name` loads the active config, which has `lamp`
- **THEN** the entities for `desk` and `shelf` are marked unavailable and not deleted, and the entity for `lamp` is published and marked available

## ADDED Requirements

### Requirement: No config files modified
The `reset` command SHALL NOT create, modify or delete any config file, including `config/default.yaml`; it only reads the config it applies.

#### Scenario: No files changed
- **WHEN** a `reset` command is executed, with or without `name`
- **THEN** no file in `config/` is created, modified or deleted
