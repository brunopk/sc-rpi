# Proposal

## Why

SC RPi's strip state (section ranges, colors, on/off) lives only in memory and is lost on
restart; the only persisted source is the hand-edited initial config, which nothing in the
app ever writes. Users want to keep several named setups (e.g. `party`, `night`) and
switch between them over MQTT without editing files on the Pi or restarting the service.

## What Changes

- Add a `save_config` command. It takes an optional `name` (the active configuration's
  name when omitted) and writes the current in-memory configuration, including the live
  section state, to `config/<name>.yaml`. Omitting `name` therefore saves the running
  state back to the active configuration, which needs `overwrite` `true` (the file
  exists) and is rejected with `RESERVED_CONFIG_NAME` while `default` is active. By default it does not overwrite: an existing name is rejected
  with a 409 `CONFIG_ALREADY_EXISTS`. An optional boolean `overwrite` argument
  (default `false`) allows replacing an existing saved config, atomically. It keeps each
  section's id and name. It doesn't change the
  running strip or publish anything to Home Assistant. Its result payload is the saved
  configuration, exactly the same payload as a `get_config` result (flat `Config`
  structure, secrets obfuscated).
- Add a `use_config` command with a **required** `name` field. It loads that file
  from the config directory into memory immediately: it rebuilds sections and strip state,
  re-renders the strip, and refreshes the Home Assistant entities. Current entities are
  marked unavailable (not deleted) and the loaded ones published as available. It doesn't modify any
  config file, so the app still boots from `config/default.yaml`.
- Keep an in-memory **active configuration**: the name of the config last loaded by
  `use_config` or a named `reset`. It is `default` at startup and is not persisted, so a
  restart goes back to `default`. A failed load leaves it unchanged, and `save_config`
  does not change it. The `status` result payload reports it as `active_configuration`.
- Extend the `reset` command with an **optional** `name` field: when omitted, it
  reloads the active configuration (`default` until a config has been loaded); when
  present, it behaves like `use_config` with that name, which becomes the active one.
- Change the `get_config` command to **require** a `name` field: it returns that saved
  file's configuration without applying it, and a missing `name` is rejected with 400
  `MISSING_CONFIG_NAME`. The live state is reported by `status` and by `save_config`.
  The result also gains `color` and `is_on` per section. MQTT settings are included, with
  secret values obfuscated: all values classified as secret, currently only the password.
- Add an optional `description` (text) to configs. `save_config` accepts it as an optional
  argument and writes it to the saved file; `get_config` results include it. A config with
  no description reports an empty one.
- Users give a config name, never a path, so no path traversal over MQTT is possible. The
  name `default` is reserved: `save_config` rejects it, even with `overwrite` set to
  `true`, so the initial file cannot be overwritten.
- Saved configs keep each section's color and on/off state. Today these values in config
  files are ignored, so a saved file would not round-trip.
- Git-ignore the `config/` directory, including `default.yaml`, since config files
  contain MQTT credentials. Only the committed example `config/default.example.yaml` is
  kept in git, so a fresh clone has a file to copy to `config/default.yaml`.
- **BREAKING**: the `get_config` payload now uses the `Config` structure, the same one as
  the saved files (keys `mqtt` and `strip` instead of `mqtt_config` and `strip_config`,
  and `mqtt.broker` instead of `mqtt.broker_config`), replacing the separate result
  models.
- **BREAKING**: `get_config` without `name` no longer returns the running configuration;
  it is rejected with 400 `MISSING_CONFIG_NAME`.
- The config key `mqtt.broker_config` is renamed to `mqtt.broker` in the config files,
  the `Config` model and the `get_config` payload.
- Add a global, retained availability topic for SC RPi (`scrpi/availability`, with LWT, birth
  and shutdown messages). Every Home Assistant entity declares it together with its own
  availability topic, so all entities become unavailable if SC RPi goes offline.
- The initial config moves from `config.yaml` to `config/default.yaml`. All configs live in
  a fixed `config/` directory, resolved from the working directory (not configurable).

Not changing: hardware-level strip settings and MQTT settings. Saved configs include them,
but `use_config` and `reset` don't apply them.

## Capabilities

### New Capabilities

- `save-config`: the `save_config` command. It accepts an optional `name` (default: the
  active configuration), an optional `description` and an optional boolean `overwrite`.
  It saves the current configuration under that name.
- `use-config`: the `use_config` command. It requires a `name` in the request body.
  Loads that saved config and applies it to the strip and the Home Assistant entities.
- `ha-availability`: the global availability topic and the cross availability of every
  entity.

### Modified Capabilities

- `reset`: now reloads the active configuration (`default` until a config has been
  loaded), or the saved config given in the optional `name` field, which becomes the
  active one.
- `get_config`: now requires a `name` field to read a saved config, and returns `color`
  and `is_on` per section, the `description`, and the MQTT settings with secret values
  obfuscated. It no longer returns the running configuration.
- `status`: its result payload now includes `active_configuration` and the running
  `description`.

## Impact

- Behavior change at startup: configured section `color`/`is_on` are now applied instead
  of ignored.
- Config file format: files gain an optional `description` field. Existing files without
  it remain valid.
- The repository's `config.yaml` becomes the committed example
  `config/default.example.yaml`; docs that mention `config.yaml` need updating.
- Home Assistant: discovery messages declare the cross availability, and `main.py` and
  `on_connect` publish the LWT, birth and shutdown messages. This must be documented in
  `doc/homeassistant.md` (entities, availability) and in `doc/commands.md`
  (`save_config`, `use_config`, and the changed `reset`, `get_config` and `status`,
  including arguments, results and the new error codes).
- Security: new file read/write driven by MQTT input; names only, never paths.