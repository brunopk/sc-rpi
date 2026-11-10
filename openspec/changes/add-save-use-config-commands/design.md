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
- Listing or deleting saved configs.
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
- `default` is reserved case-insensitively for saving only (macOS and Windows filesystems
  are case-insensitive, so `Default` would otherwise hit `default.yaml`). `validate_name`
  checks the alphabet and length; `save` additionally rejects the reserved name. Loading
  `default` is allowed.
- Alternative: accept paths and sandbox them with `resolve()` + `is_relative_to`.
  Rejected: larger attack surface for no user benefit.

### 2. Save does not overwrite unless asked, atomically

`save(name, config, overwrite=False)` runs these steps:

1. Write the YAML to a temporary file in `config/` (mode `0600`, since it holds MQTT
   credentials).
2. Give it its final name:
   - `overwrite=False`: `os.link(tmp, target)`.
   - `overwrite=True`: `os.replace(tmp, target)`.
3. Delete the temporary name (not needed after `os.replace`, which consumes it).

`os.link` creates a second name for the same file contents and, unlike `os.rename`, fails
with `FileExistsError` when the target exists instead of replacing it. `os.replace`
atomically swaps the target, so a reader or a crash sees either the old or the new
complete file, never a partial one.

- With `overwrite=False`, `FileExistsError` maps to 409 `CONFIG_ALREADY_EXISTS`.
- `overwrite` is an optional boolean argument of `save_config`, default `false`. It only
  matters when the name already exists; for a new name both values behave the same.
- The reserved name check runs before and regardless of `overwrite`, so `default.yaml`
  can never be replaced.
- `SaveConfig` resolves the name before calling `store.save`: the given `name`, or
  `hw_controller.active_configuration` when `name` is omitted. From there it is the same
  flow as a given name, so the reserved check, the `overwrite` rule and name validation
  apply unchanged. While `default` is active (startup), omitting `name` always fails with
  `RESERVED_CONFIG_NAME`. `save_config` still does not change the active configuration.
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

- `Config` stays the immutable initial configuration, passed to commands as today. It gains
  an optional `description: str = ""`, so existing files without it remain valid.
- `HardwareController` keeps creating `SectionsController` and delegating to it.
- It gains three methods and one attribute:
  - `get_current_config() -> Config`: the initial `Config` with `strip.sections` and
    `description` taken from the live state at the time of the call. Changes made by
    earlier commands (`edit_section`, `turn_section_off`, `use_config`) are included.
    `save_config` uses it; `get_config` does not, since it only reads saved files.
  - `prepare_config(loaded: Config) -> list[SectionInternalRepresentation]`: validates
    and builds the new sections without changing any state (see decision 4).
  - `apply_prepared(sections: list[SectionInternalRepresentation], description: str,
    active_configuration: str)`: renders the prepared sections and then replaces the
    sections, the description and the active configuration (see decision 4).
  - `active_configuration: str`: the name of the config last loaded by `use_config` or a
    named `reset`. It starts as `"default"`, lives in memory only (a restart goes back to
    `"default"`), and only `apply_prepared` changes it, so it changes only when the
    whole apply succeeded. `save_config` does not change it.

Details:

- The description and the active configuration name are stored on `HardwareController` as
  plain configuration metadata, and the docstring says so. Each is one string, so they do
  not justify a new class.
- Section names are part of the live state:
  - `SectionsController` stores the name of each section, taken from the config.
  - `SectionInternalRepresentation` gains a `name` field, set by `SectionsController`
    when it returns sections.
- Commands read live sections from `hw_controller`, never from the initial
  `config.strip.sections` (see Risks).
- Alternative: a `RunningConfig` class replacing `Config` in commands. Rejected for now:
  it needs new wiring in every command, and both it and `HardwareController` would
  reference the same `SectionsController`, leaving unclear which one owns it.
- Alternative: put the description on `SectionsController`. Rejected: it is not section
  state.

### 4. Apply a config in two steps: `prepare_config`, then `apply_prepared`

Applying a config takes two `HardwareController` calls, so the command can do everything
that may fail before the strip is touched:

1. `prepare_config(loaded)` builds the new sections in local variables from the loaded
   config's sections, validated against the **running** `strip_length` (hardware settings
   are not reapplied). It returns the built sections, the same type `list_sections()`
   returns, and changes no state.
2. The caller builds the command result and the Home Assistant messages from the prepared
   sections.
3. `apply_prepared(sections, description, active_configuration)` takes the prepared
   sections, the loaded config's description and the name that was loaded (plain strings
   that need no building). It renders the strip from the sections, without touching the
   controller's state. Only if the render raised no exception, it replaces the controller's
   internal sections, the description and the active configuration.

- Two patterns coexist, one per kind of command:
  - `edit_section`, `turn_section_on` and `turn_section_off` keep their pattern: change
    the live state, build the result, call `hw_controller.render()` last. They are not
    modified.
  - `use_config` and `reset` use `prepare_config` and `apply_prepared`, because they
    replace all sections and must leave nothing changed on failure.
  - A comment inside `run()` of `UseConfig` and `Reset` explains why they use
    `prepare_config` and `apply_prepared`, so the choice is visible in the code where it
    is made.
- `apply_prepared` is the last call in `run()`, in place of the `hw_controller.render()`
  call that other commands make, so the rule that rendering comes last still holds.
- A render that "succeeds" means `setPixelColor` and `show()` raised no exception. The
  controller cannot check what the LEDs show.
- If the build fails (for example overlapping sections, or a section beyond
  `strip_length`), nothing was modified. The `ApiError` is reported as `INVALID_CONFIG`
  (500).
- If building the result or the Home Assistant messages fails, the strip was not touched.
- If the render fails, the controller state was never touched, so sections, description
  and the error result agree: nothing changed.
- The replacement in step 3 is a plain in-memory assignment, so no failure is possible
  after the strip has been rendered.
- A file that cannot be parsed fails earlier, in `store.load`, with the same code.
- This removes the need for the rollback TODO in `reset`: state is replaced only after the
  build and the render succeeded, so a failure leaves nothing to roll back.
- The build must reject every kind of overlap, including sections that share a boundary
  LED or enclose another section (for example, with an existing section at LEDs 10-20,
  a new section at 20-30 shares LED 20, and one at 5-25 encloses it). Today's check in
  `SectionsController` does not cover all of them, and a bad saved file must not be
  accepted as valid.
- Alternative: replace the state first and restore the previous state if the render
  fails. Rejected: it needs a copy of all section state and the restore can fail too,
  which brings back the rollback problem.
- The `SectionsController` instance is created once and never replaced. Commands run on
  one worker thread, so no locking is needed.
- Alternative: build a new `SectionsController` and swap the instance. Rejected: every
  holder would have to avoid keeping a reference to it.

### 5. One helper for `use_config` and `reset`: `apply_named_config`

A helper `apply_named_config(hw_controller, command_name, config_name, brightness)` (in
`utils/commands/`) runs these steps:

1. Validate the name.
2. `load` the config (`sc_rpi/utils/config/store.py`).
3. Read the sections currently running from `hw_controller`.
4. `hw_controller.prepare_config(loaded)`, with the `Config` loaded in step 2. It builds
   the new sections and description from it.
5. Build the result dict: the SC RPi result entry first, then the Home Assistant messages
   from `build_ha_refresh_messages` (decision 6), called with the sections read in step 3,
   the prepared sections and the brightness.
6. `hw_controller.apply_prepared(sections, loaded.description, config_name)`, the last
   step: it renders the prepared sections on the strip and then replaces the controller's
   state, including the active configuration. The commands return the result right after,
   so nothing that can fail runs once the strip has changed.

- `UseConfig` and `Reset` call it, passing their hardware controller, their
  `command_name` and the default section brightness from their config; `Reset` passes
  `hw_controller.active_configuration` as `config_name` when the `reset` command omits
  the config name. Reloading the active config sets the same name again.
- If the active configuration's file is missing or invalid, `store.load` fails with
  `CONFIG_NOT_FOUND` or `INVALID_CONFIG` before anything is changed, so `reset` without
  `name` leaves the state and the active name as they were.
- The helper takes these values as arguments instead of the command, so it does not
  depend on the private attributes of `Command` and can be tested without a command
  instance.
- The SC RPi result entry is `build_status_result(...)` with the given `command_name`, so
  results are identical except for the name.
- The Home Assistant messages use the prepared sections, which are the ones
  `apply_prepared` renders, so the messages and the result payload describe what was
  rendered.
- The `Worker` publishes the dict in insertion order, so the helper puts the entries in
  the order wanted and no other code orders messages.

### 6. Home Assistant entity refresh

`build_ha_refresh_messages(previous_sections, new_sections, brightness)` in
`utils/homeassistant.py` returns the Home Assistant messages (topic → payload) for
replacing the published entities. `previous_sections` are the sections published before
and `new_sections` the ones to publish. The messages are in this order, so each entity
exists and is available before its state arrives:

1. `offline` for each section that was running before the apply and whose id is not in
   the loaded config, published to that section's availability topic.
2. Discovery for each loaded section, including its availability topic.
3. `online` for each loaded section, published to that section's availability topic.
4. State for each loaded section: ON or OFF (from `is_on`), color and brightness
   (`default_section_brightness`).

- When the same config is applied again (for example `reset` after edits), its section
  ids are unchanged, so no `offline` message is sent for them. A topic can appear only
  once in the result dict, and skipping it avoids relying on insertion order to let
  `online` win.
- At startup the initial sections go through the same message sequence as an apply, minus
  the `offline` step: discovery, `online`, then state. `build_ha_refresh_messages` serves
  both cases, with no previous sections at startup. `Worker` calls it and publishes the
  returned dict in order, replacing `_publish_ha_entities`. No SC RPi result entry is
  involved.
- Alternative: delete old entities with an empty retained discovery payload. Rejected by
  the proposal (history and UI customization would be lost).
- Each entity has its own availability topic,
  `scrpi/homeassistant/<object_id>/availability`, set in its discovery message
  (`availability_topic`). The payloads are the plain strings `online` and `offline`, which
  are Home Assistant's defaults.
- Availability messages are not retained, like the other messages today (discovery retain
  is an existing TODO). Making them retained would need a retain flag in the command
  result and the `Worker`, so it is out of scope.
- Availability is plain online/offline per entity; no MQTT Last Will and Testament is added.

### 7. Result payload is the `Config` model

This resolves the TODO in `commands/get_config/command.py` about duplicated config models.

- Both commands return `mask_secrets(config)` as the flat payload, with no extra or
  nested keys. `get_config` takes the `Config` from `store.load(name)`; `save_config`
  from `hw_controller.get_current_config()`, the same one it writes to the file.
- `get_config` requires `name`; without it, it fails with `MISSING_CONFIG_NAME` (400)
  like `use_config`. The live state is read with `status`.
- `mask_secrets` returns a copy with every secret value replaced by a placeholder. The
  secret fields are listed in that one function (today only the MQTT password); all
  other values, including the MQTT username, are returned as they are. Adding a secret
  later means adding it to that list, and no command can leak a secret by forgetting.
  A test fills every field in that list with a distinctive value and checks that none of
  them appears in the masked output.
- The saved YAML, the `get_config` payload and the `save_config` payload share one
  structure by construction, so a saved config read back with `get_config` matches what
  was saved.
- `build_status_result` adds `active_configuration` and `description` (from
  `hw_controller`) to `StatusResultPayload`, so the `status` result reports them. Every other result that lists
  sections is built the same way and carries it too, which keeps `use_config` and `reset`
  results identical.
- **BREAKING** for `get_config` consumers: payload keys follow the `Config` model.
  `mqtt_config` becomes `mqtt` (and the `broker_config` inside it becomes `broker`), and
  `strip_config` becomes `strip`. `get_config` without `name` is now an error instead of
  returning the running configuration. Recorded in the proposal and in `doc/commands.md`.
- Alternative: keep the old keys with mashumaro aliases. Rejected: it keeps a mapping
  layer and leaves the duplication TODO half resolved.

### 8. Errors

New error codes are raised as `ApiError`, so `map_exception` needs no new path. The
codes and statuses are defined in the specs.

## Risks / Trade-offs

- [Secrets in `config/`] → git-ignore the directory, create saved files with `0600`.
- [Saved config's strip length differs from hardware] → sections are validated against
  the running strip; mismatches fail as `INVALID_CONFIG` with state unchanged.
- [HA offline/online messages are not retained or reliable over reconnects] → acceptable
  for now; the next apply or boot re-publishes.
- [Results built from the initial config instead of the live state] → results must come
  from `hw_controller` (`list_sections()` or `get_current_config()`), never from
  `config.strip.sections`; `test_result_ignores_initial_config` tests check this for every command whose result
  includes sections.
- [The existing overlap check in `SectionsController` misses boundary and enclosing
  overlaps (with an existing section at LEDs 10-20, a new one at 20-30 shares LED 20
  and one at 5-25 encloses it), so `INVALID_CONFIG` would not trigger for them] → the build in decision 4
  must use a check that covers all overlaps; covered by an apply test with each kind
  of overlap.
- [Storing the real `is_on` in the ordered list may expose related bugs in
  `turn_section_off`, which also updates that list] → fix them together; covered by the
  turn on/off command tests and a new save/load round-trip test.

## Migration Plan

- Commit the existing `config.yaml` as `config/default.example.yaml` and git-ignore
  `config/`, so credentials stay out of git. A fresh clone copies the example.
