# Proposal

## Why

SC RPi's strip state (section ranges, colors, on/off) lives only in memory and is lost on
restart; the only persisted source is the hand-edited boot config, which nothing in the
app ever writes. Users want to keep several named setups (e.g. `party`, `night`) and
switch between them over MQTT without editing files on the Pi or restarting the service.

## What Changes

- Add a `save_config` command. It requires a `config_name` in the request body and writes
  the current in-memory configuration, including the live section state, to
  `config/<config_name>.yaml`. It never overwrites: an existing name is rejected with a 409
  `CONFIG_ALREADY_EXISTS`. It gives sections the id `<config_name>_section_<n>` (names are
  kept) in the saved file only, so each config has its own Home Assistant entities once
  loaded. It doesn't change the running strip or publish anything to Home Assistant. Its
  result includes the saved configuration (same structure
  as `get_config`, password obfuscated).
- Add a `use_config` command with a **required** `config_name` field. It loads that file
  from the config directory into memory immediately: it rebuilds sections and strip state,
  re-renders the strip, and refreshes the Home Assistant entities. Current entities are
  marked unavailable (not deleted) and the loaded ones published as available. It doesn't modify any
  config file, so the app still boots from `config/default.yaml`.
- Extend the `reset` command with an **optional** `config_name` field: when omitted, it
  loads `config/default.yaml`; when present, it behaves like `use_config` with that name.
- Extend the `get_config` command with an **optional** `config_name` field: when present,
  it returns that saved file's configuration without loading it. The result also gains
  `color` and `is_on` per section. MQTT settings are included, with the password
  obfuscated.
- Add an optional `description` (text) to configs. `save_config` accepts it as an optional
  argument and writes it to the saved file; `get_config` results include it. A config with
  no description reports an empty one.
- Users give a config name, never a path, so no path traversal over MQTT is possible. The
  name `default` is reserved: `save_config` rejects it so the boot file cannot be
  overwritten.
- Saved configs keep each section's color and on/off state. Today these values in config
  files are ignored, so a saved file would not round-trip.
- Git-ignore the `config/` directory, including `default.yaml`, since config files
  contain MQTT credentials.
- **BREAKING**: the boot config moves from `config.yaml` to `config/default.yaml`. All
  configs live in a fixed `config/` directory, resolved from the working directory (not
  configurable).

Not changing: hardware-level strip settings and MQTT settings. Saved configs include them,
but `use_config` and `reset` don't apply them.

## Capabilities

### New Capabilities

- `save-config`: the `save_config` command. It requires a `config_name` in the request
  body and accepts an optional `description`. It saves the current configuration under
  that name.
- `use-config`: the `use_config` command. It requires a `config_name` in the request body.
  Loads that saved config and applies it to the strip and the Home Assistant entities.

### Modified Capabilities

- `reset`: now loads `config/default.yaml`, or the saved config given in the optional
  `config_name` field.
- `get_config`: now accepts an optional `config_name` field to read a saved config, and
  returns `color` and `is_on` per section, the `description`, and the MQTT settings with
  the password obfuscated.

## Impact

- Behavior change at startup: configured section `color`/`is_on` are now applied instead
  of ignored.
- Config file format: files gain an optional `description` field. Existing files without
  it remain valid.
- Existing deployments must move `config.yaml` to `config/default.yaml`; docs that
  mention `config.yaml` need updating.
- Home Assistant: discovery messages gain an availability topic, so entities can be marked
  unavailable. Loading a saved config (`use_config`, or `reset` with a name) changes
  section ids to that config's ids, so entities, automations and history tied to the old
  ids stop working. This must be documented in
  `doc/homeassistant.md` (entities, availability, id change) and in `doc/commands.md`
  (`save_config`, `use_config`, and the changed `reset` and `get_config`, including
  arguments, results and the new error codes).
- Security: new file read/write driven by MQTT input; names only, never paths.