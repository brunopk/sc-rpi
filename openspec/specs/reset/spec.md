# reset Specification

## Purpose

Lets users restore the strip to the state defined by the loaded configuration.

## Requirements

### Requirement: Reset rebuilds sections from configuration
The `reset` command SHALL rebuild the strip's sections from the configuration loaded in memory, re-render the strip, and publish a successful status result listing the resulting sections to the result topic.

#### Scenario: Reset after edits
- **WHEN** sections have been edited or turned off and a `reset` command is received
- **THEN** the sections match the configured section definitions and a successful result is published

### Requirement: Reset updates Home Assistant entities
The `reset` command SHALL publish a state for every section to its Home Assistant state topic, using the section's color and the configured default section brightness.

#### Scenario: Entities refreshed
- **WHEN** a `reset` command is received
- **THEN** each section's Home Assistant state topic receives an ON state with the section's color
