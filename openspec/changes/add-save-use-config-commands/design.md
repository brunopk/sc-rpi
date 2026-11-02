# Design

## Context

See proposal.md for motivation and the specs for requirements.
Current state that shapes the approach:

- `Config` is a mashumaro dataclass loaded once in `main.py` from `config.yaml` and shared
  by `Worker`, `HardwareController`, `SectionsController` and every command. Nothing
  mutates it.
- `SectionsController` owns the live section state, but it is built from
  `config.strip.sections` and ignores each section's `color`/`is_on` (it hardcodes
  `is_on=False`; `_insert_section` also always inserts `True` into `_is_on`, which
  differs from `_is_on_by_id`). `reset_sections()` re-reads the same shared `Config`.
- `get_config` currently maps `config.strip.sections`, which does not reflect live edits.
- Home Assistant entities are published only at boot, by `Worker._publish_ha_entities`
  (private to the worker). `reset` publishes only states. Discovery messages have no
  availability topic.
- Commands run only on the worker thread. `run()` returns `{topic: payload}` and the
  worker publishes the entries in dict (insertion) order.
- `reset` has a TODO about rollback: it mutates state before anything can fail.

## Goals / Non-Goals

**Goals:**
- Applying a config is all-or-nothing: any failure leaves sections, strip and HA untouched.
- One implementation of "apply config" shared by `use_config` and `reset`.
- All name-to-path handling goes through the `sc_rpi/utils/config/store.py` module,
  so no command builds a file path itself.
- One model for configuration: the saved file and the `get_config`/`save_config` payloads
  use the same `Config` dataclass.

**Non-Goals:**
- Hot-applying strip hardware or MQTT settings.
- Listing or deleting saved configs, or overwriting an existing one.
- Cross-process locking of the `config/` directory (single service instance assumed).

## Decisions

### 1. `sc_rpi/utils/config/store.py` module owns names, paths and file I/O

New module with `validate_name`, `path_for(name)`, `load(name)` and `save(name, config)`.

- The directory is the constant `config/`, resolved from the CWD.
- `load_configurations()` reads `config/default.yaml` through the same loader, so boot and
  `use_config` parse identically.
- Name check uses `re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name)`. Only that alphabet is
  accepted, so no separators, dots or `..` can reach the filesystem and no path
  resolution or prefix comparison is needed.
- `default` is reserved case-insensitively (macOS and Windows filesystems are
  case-insensitive, so `Default` would otherwise hit `default.yaml`).
- Alternative: accept paths and sandbox them with `resolve()` + `is_relative_to`.
  Rejected: larger attack surface for no user benefit.

### 2. Save never overwrites, atomically

`save` runs these steps:

1. Write the YAML to a temporary file in `config/` (mode `0600`, since it holds MQTT
   credentials).
2. Give it its final name with `os.link(tmp, target)`.
3. Delete the temporary name.

`os.link` creates a second name for the same file contents and, unlike `os.rename`, fails
with `FileExistsError` when the target exists instead of replacing it.

- That error maps to 409 `CONFIG_ALREADY_EXISTS`.
- There is no check-then-write race between concurrent saves of the same name.
- A crash mid-write leaves only the temporary file, never a half-written config under a
  real name.
- Alternative: `open(path, "x")`. Simpler, but a crash mid-write leaves a truncated file
  that blocks the name and later fails with `INVALID_CONFIG`.
- The file keeps the real secret values (it must be a valid config). Only command
  results obfuscate them.

### 3. `HardwareController` exposes the current configuration

Commands already receive `hw_controller` to read and change the live strip state. It also
becomes the place to get and replace the configuration:

- `Config` stays the immutable boot configuration, passed to commands as today. It gains
  an optional `description: str = ""`, so existing files without it remain valid.
- `HardwareController` keeps creating `SectionsController` and delegating to it.
- It gains two methods:
  - `get_current_config() -> Config`: the boot `Config` with `strip.sections` and
    `description` taken from the live state at the time of the call. Changes made by
    earlier commands (`edit_section`, `turn_section_off`, `use_config`) are included.
    `get_config` and `save_config` both use it.
  - `apply_config(loaded: Config)`: replaces the sections and the description (see
    decision 4).

Details:

- The description is stored on `HardwareController` as plain configuration metadata, and
  the docstring says so. It is one string, so it does not justify a new class.
- Section names are part of the live state:
  - `SectionsController` stores the name of each section, taken from the config.
  - `SectionInternalRepresentation` gains a `name` field, set by `SectionsController`
    when it returns sections.
- Commands read live sections from `hw_controller`, never from the boot
  `config.strip.sections` (see Risks).
- Alternative: a `RunningConfig` class replacing `Config` in commands. Rejected for now:
  it needs new wiring in every command, and both it and `HardwareController` would
  reference the same `SectionsController`, leaving unclear which one owns it.
- Alternative: put the description on `SectionsController`. Rejected: it is not section
  state.

### 4. Apply = build on the side, then replace in place

`HardwareController.apply_config(loaded: Config)` runs these steps:

1. Call `SectionsController.replace_sections(...)` with the loaded config's sections.
2. Inside it, build the new section lists in local variables, validated against the
   **running** `strip_length` (hardware settings are not reapplied).
3. Only if the build succeeded, replace the controller's internal state with the new
   lists.
4. Replace the description.

- If the build fails (for example overlapping sections, or a section beyond
  `strip_length`), nothing was modified. The `ApiError` is reported as `INVALID_CONFIG`
  (500).
- A file that cannot be parsed fails earlier, in `store.load`, with the same code.
- This removes the need for the rollback TODO in `reset`: state is replaced only after the
  build succeeded, so a failure leaves nothing to roll back.
- The `SectionsController` instance is created once and never replaced. Commands run on
  one worker thread, so no locking is needed.
- Alternative: build a new `SectionsController` and swap the instance. Rejected: every
  holder would have to avoid keeping a reference to it.

### 5. Shared apply logic for `use_config` and `reset`

A helper `apply_named_config(cmd, name)` (in `utils/commands/`) runs these steps:

1. Validate the name.
2. `load` the config (`sc_rpi/utils/config/store.py`).
3. `hw_controller.apply_config(...)`.
4. Build the result topics.

- `UseConfig` and `Reset` call it; `Reset` passes `"default"` when `name` is
  absent.
- The result is `build_status_result(...)` with the caller's `command_name`, so results
  are identical except for the name.

### 6. Home Assistant messages for an apply

When `use_config` or `reset` applies a config, `apply_named_config` returns the Home Assistant messages in this order, so each entity exists and is available before its state arrives:    

1. `offline` for each section that was running before the apply and whose id is not in
   the loaded config.
2. Discovery for each new section.
3. `online`.
4. State for each loaded section: ON or OFF (from `is_on`), color and brightness
   (`default_section_brightness`).

`build_ha_refresh_messages(previous_sections, new_sections, brightness)` in
`utils/homeassistant.py` returns the Home Assistant messages (topic → payload) in the
order above. `apply_named_config` reads the previous sections before applying the config.
It then builds the command result: the SC RPi result entry first, followed by these
messages. The `Worker` publishes the dict in insertion order, so no other code orders
messages.

- When the same config is applied again (for example `reset` after edits), its section
  ids are unchanged, so no `offline` message is sent for them. A topic can appear only
  once in the result dict, and skipping it avoids relying on insertion order to let
  `online` win.
- At startup the boot sections go through the same message sequence as an apply, minus
  the `offline` step: discovery, `online`, then state. `build_ha_refresh_messages` serves
  both cases, with no previous sections at startup.
- Alternative: delete old entities with an empty retained discovery payload. Rejected by
  the proposal (history and UI customization would be lost).
- Availability is plain online/offline per entity; no MQTT Last Will and Testament is added.

### 7. Result payload is the `Config` model

This resolves the TODO in `commands/get_config/command.py` about duplicated config models.

- The payload of `get_config` and `save_config` is `hw_controller.get_current_config()`
  (or the loaded named `Config`) passed through `mask_secrets(config) -> Config`.
- `mask_secrets` returns a copy with every secret value replaced by a placeholder. The
  secret fields are listed in that one function (today only the MQTT password); all
  other values, including the MQTT username, are returned as they are. Adding a secret
  later means adding it to that list, and no command can leak a secret by forgetting.
- The saved YAML, the `get_config` payload and the `save_config` payload share one
  structure by construction, so a saved config read back with `get_config` matches what
  was saved.
- `save_config`'s payload nests the configuration: `{"name": ..., "config": <Config>}`,
  so `payload.config` equals the `get_config` payload.
- **BREAKING** for `get_config` consumers: payload keys follow `Config` (`mqtt`, `strip`,
  `mqtt.broker_config`) instead of `mqtt_config`, `strip_config`. Recorded in the
  proposal and in `doc/commands.md`.
- Alternative: keep the old keys with mashumaro aliases. Rejected: it keeps a mapping
  layer and leaves the duplication TODO half resolved.

### 8. Errors

New error codes are raised as `ApiError`, so `map_exception` needs no new path. The
codes and statuses are defined in the specs.

## Risks / Trade-offs

- [Secrets in `config/`] → git-ignore the directory, create saved files with `0600`.
- [Loading a different config replaces the running section ids, orphaning Home Assistant
  entities and automations tied to the old ids] → documented; the old entities are only
  marked unavailable, not deleted.
- [Saved config's strip length differs from hardware] → sections are validated against
  the running strip; mismatches fail as `INVALID_CONFIG` with state unchanged.
- [HA offline/online messages are not retained or reliable over reconnects] → acceptable
  for now; the next apply or boot re-publishes.
- [Commands could read the boot section list (`config.strip.sections`), which does not
  reflect edits] → live sections must come from `hw_controller`; add a test that edits a
  section and then checks the `get_config` result.
- [Storing the real `is_on` in the ordered list may expose related bugs in
  `turn_section_off`, which also updates that list] → fix them together; covered by the
  turn on/off command tests and a new save/load round-trip test.
