# Spec Delta

## Purpose

Lets Home Assistant know when SC RPi, or one of its sections, is not available, so entities do not show stale states.

## ADDED Requirements

### Requirement: Global availability topic
SC RPi SHALL report its own availability on the topic `scrpi/availability` with the payloads `online` and `offline`, always published with the retain flag. Before connecting to the broker, it SHALL register `offline` as its Last Will and Testament (LWT) on that topic, retained. After every successful connection, it SHALL publish `online` there. On a controlled shutdown, it SHALL publish `offline` there, and wait for the publication, before disconnecting from the broker.

#### Scenario: Birth message
- **WHEN** SC RPi connects to the broker (including a reconnection)
- **THEN** a retained `online` message is published on `scrpi/availability`

#### Scenario: Abrupt failure
- **WHEN** the connection to the broker drops without a clean disconnect
- **THEN** the broker publishes the retained `offline` Last Will on `scrpi/availability`

#### Scenario: Controlled shutdown
- **WHEN** SC RPi stops in a controlled way
- **THEN** a retained `offline` message is published on `scrpi/availability` before the MQTT disconnect

### Requirement: Cross availability in discovery
The discovery message of every entity SHALL declare `availability_mode` as `all` and an `availability` list with two topics: `scrpi/availability` and the entity's own availability topic (`scrpi/homeassistant/<id>/availability`). It SHALL NOT use `availability_topic`. The entity is therefore available only when both topics report `online`.

#### Scenario: Discovery lists both topics
- **WHEN** the discovery message for section `desk` is published
- **THEN** it contains `"availability_mode": "all"` and an `availability` list with the topics `scrpi/availability` and `scrpi/homeassistant/desk/availability`, and no `availability_topic`

#### Scenario: SC RPi goes offline
- **WHEN** `scrpi/availability` is `offline`
- **THEN** every entity is unavailable, whatever its own availability topic says

#### Scenario: Section removed
- **WHEN** a section's entity is marked `offline` on its own availability topic while `scrpi/availability` is `online`
- **THEN** only that entity is unavailable
