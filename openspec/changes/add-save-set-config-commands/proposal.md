# Proposal

## Why

SC RPi's strip state (section ranges, colors, on/off) lives only in memory and is lost on
restart; the only persisted source is the hand-edited `config.yaml`, which nothing in the
app ever writes. Users want to keep several named setups (e.g. `party`, `night`) and
switch between them over MQTT without editing files on the Pi or restarting the service.

## What Changes

- Add a `save_config` command that writes the current in-memory configuration (including
  the live section state) to a user-chosen file name inside a new config directory.
- Add a `set_config` command that loads a file from that directory into memory
  immediately: it rebuilds sections and strip state, re-renders the strip, and refreshes
  the Home Assistant entities. The choice is **not** persisted across restarts (the app
  still boots from `config.yaml`).
- Add a `config_dir` setting (optional, defaults to `configs`, resolved from the working
  directory) naming the directory where these files live.
- Users choose only a file **name**, never a path. Names are validated and the server adds
  the `.yaml` extension, so no path traversal over MQTT is possible.
- Make section initialization honor the `color` and `is_on` values stored in config
  sections. Today `SectionsController._initialize_sections()` ignores them, so a saved
  file would not round-trip.
- Two separate commands: there is no combined save-and-set and no "active file" concept.
- Add new error codes `CONFIG_NOT_FOUND` and `INVALID_CONFIG`, document the commands in
  `doc/commands.md`, and git-ignore the config directory (saved files contain MQTT
  credentials).

Not changing: `get_config` output, the boot-time config source, and hardware-level strip
settings (they cannot change without re-creating the `PixelStrip`).

## Capabilities

### New Capabilities

- `save-config`: the `save_config` command, the config directory, file-name validation,
  and the on-disk format of saved files.
- `set-config`: the `set_config` command, including validation of the file, atomic
  switching of in-memory state, strip re-render, and Home Assistant entity refresh.

### Modified Capabilities

<!-- None: openspec/specs/ is empty, so there are no existing requirements to modify. -->

## Impact

- New packages `src/sc_rpi/commands/save_config/` and `src/sc_rpi/commands/set_config/`
  (auto-listed by `help`, which discovers command directories), imported in
  `commands/__init__.py`.
- `config/main.py` (new optional `config_dir`), `utils/config/main.py` (save helper and
  name-aware load), `controllers/sections_controller.py` and
  `controllers/hardware_controller.py` (honor stored color/is_on, atomic swap),
  `enums/error_code.py`.
- Behavior change at startup: configured section `color`/`is_on` are now applied instead
  of ignored.
- Security: new filesystem write/read driven by MQTT input; mitigated by name-only input,
  strict validation, and owner-only file permissions.
- No new dependencies (PyYAML is already used by the config loader).
- Docs: `doc/commands.md`, README configuration note; `.gitignore`.