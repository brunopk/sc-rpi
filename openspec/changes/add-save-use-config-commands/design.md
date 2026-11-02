# Design

## Context

See proposal.md for motivation and the specs for requirements. Current state that shapes the approach:

- `Config` is a mashumaro dataclass loaded once in `main.py` from `config.yaml` and shared
  by `Worker`, `HardwareController`, `SectionsController` and every command. Nothing
  mutates it.
- `SectionsController` owns the live section state, but it is built from
  `config.strip.sections` and ignores each section's `color`/`is_on` (it hardcodes
  `is_on=False`; `_insert_section` also always inserts `True` into `_is_on`, which
  disagrees with `_is_on_by_id`). `reset_sections()` re-reads the same shared `Config`.
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
- Name-to-path mapping lives in one place and cannot escape `config/`.

**Non-Goals:**
- Hot-applying strip hardware or MQTT settings.
- Listing or deleting saved configs, or overwriting an existing one.
- Cross-process locking of the `config/` directory (single service instance assumed).

## Decisions

### 1. `ConfigStore` module owns names, paths and file I/O

New `sc_rpi/utils/config/store.py` with `validate_name`, `path_for(name)`, `load(name)`,
`save(name, config)`. The directory is a constant `config/` resolved from the CWD.
`load_configurations()` reads `config/default.yaml` through the same loader, so boot and
`use_config` parse identically.

- Name check uses `re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name)` (`fullmatch`, not `$`,
  which accepts a trailing newline). Because only that alphabet is accepted, no
  separators, dots or `..` can reach the filesystem; we don't rely on resolving paths and
  comparing prefixes.
- `default` is reserved case-insensitively (macOS and Windows filesystems are
  case-insensitive, so `Default` would otherwise hit `default.yaml`).
- Alternative considered: accept paths and sandbox them with `resolve()` +
  `is_relative_to`. Rejected: larger attack surface for no user benefit.

### 2. Save never overwrites, atomically

`save` serializes to a temp file in `config/` (mode `0600`, since it holds MQTT
credentials) and publishes it with `os.link(tmp, target)` then removes the temp file.
`link` fails with `FileExistsError` if the target exists, which maps to 409
`CONFIG_ALREADY_EXISTS`; there is no check-then-write race, and readers never see a
half-written file.
- Alternative: `open(path, "x")`. Simpler, but a crash mid-write leaves a truncated file
  that blocks the name and later fails with `INVALID_CONFIG`.
- The file keeps the real MQTT password (it must be a valid config). Only command
  results obfuscate it.

### 3. Running config is composed, not stored

The shared `Config` stays immutable. The "running configuration" used by `get_config` and
`save_config` is built on demand: static parts from `Config` + sections from
`HardwareController.list_sections()` (id, name, start, end, color, `is_on`) + the running
description. The description is held by `HardwareController` next to the sections, and
replaced when a config is applied.

- `SectionInternalRepresentation` has no `name`; names are needed for discovery and for
  save. The controller keeps a name per section id (loaded from the config, edited never)
  so the live state is the single source of truth.
- Alternative: mutate `Config.strip.sections`. Rejected: shared across threads, and the
  rule in CLAUDE.md is no mutable state beyond dataclass fields.

### 4. Apply = build new state, then swap

`HardwareController.apply_config(loaded: Config)` builds a fresh `SectionsController`
from the loaded config's sections, validated against the **running** `strip_length`
(hardware settings are not reapplied). Only after construction succeeds does it swap the
controller and description. Any `ApiError` or parse error during the build is converted to
`INVALID_CONFIG` (500). This also resolves the rollback TODO in `reset`.
`reset_sections()` is replaced by this path (`reset` without a name loads
`config/default.yaml` from disk, so edits to the file apply without a restart).
Section `color` and `is_on` are now honored in `_initialize_sections` (and the
`_insert_section` `is_on` inconsistency is fixed as part of it), which is also what makes
startup apply them.

### 5. Shared apply logic for `use_config` and `reset`

A helper `apply_named_config(cmd, name)` (in `utils/commands/`) does: validate name →
`ConfigStore.load` → `hw_controller.apply_config` → build result topics. `UseConfig` and
`Reset` call it; `Reset` passes `"default"` when `config_name` is absent. The result is
`build_status_result(...)` with the caller's `command_name`, so results are identical
except for the name. `render()` is the last call, as CLAUDE.md requires.

`config_name` on `use_config`/`save_config` is declared `str | None = None` and checked in
`validate()`, so a missing value yields `MISSING_CONFIG_NAME` rather than a generic parse
error.

### 6. Home Assistant publishing moves out of the worker

Extract discovery/state building from `Worker._publish_ha_entities` into
`utils/homeassistant.py` (discovery message with `availability_topic`, availability
payloads, state), used by both boot and the apply helper. New
`build_ha_availability_topic(object_id)` in `topic_utils.py`; `HAMQTTDiscoveryMessage`
gains optional `availability_topic`.

Result dict order for an apply: `offline` for old ids no longer present → discovery for
each new section → `online` → state. Ids present before and after (e.g. default →
default) skip `offline`, because a topic can appear only once in the dict and it would
flap. Boot also publishes `online`. The state uses `default_section_brightness` and the
section's `is_on`, as in the specs.
- Alternative: delete old entities with an empty retained discovery payload. Rejected by
  the proposal (history and UI customization would be lost).
- Availability is plain online/offline per entity; no LWT is added.

### 7. Result models

Extend the existing `get_config` result models with `color`, `is_on` and `description`
instead of adding a parallel model. A single mapper `Config + sections → GetConfigResult`
serves `get_config` (running or named) and `save_config`, which guarantees the "same
structure" scenarios. The MQTT password is obfuscated inside that mapper, so no command
can leak it by forgetting. `save_config`'s payload adds `config_name`.

### 8. Errors

Add `MISSING_CONFIG_NAME` (400), `INVALID_CONFIG_NAME` (400), `RESERVED_CONFIG_NAME` (400),
`CONFIG_NOT_FOUND` (404), `CONFIG_ALREADY_EXISTS` (409), `INVALID_CONFIG` (500) to
`ErrorCode`. Raised as `ApiError`, so `map_exception` needs no new path.

## Risks / Trade-offs

- [`config.yaml` → `config/default.yaml` breaks deployments] → document the move in
  `doc/*`, and fail at startup with a message naming the expected path.
- [Secrets in `config/`] → git-ignore the directory, create saved files with `0600`.
- [Section ids change on load, orphaning HA entities/automations] → documented; old
  entities are only marked unavailable, not deleted.
- [Saved config's strip length differs from hardware] → sections are validated against
  the running strip; mismatches fail as `INVALID_CONFIG` with state unchanged.
- [HA offline/online messages are not retained or reliable over reconnects] → acceptable
  for now; the next apply or boot re-publishes.
- [Fixing `_is_on` handling touches existing turn on/off behavior] → covered by existing
  command tests plus new ones for a save/load round-trip.

## Migration Plan

1. Move `config.yaml` to `config/default.yaml` on each Pi (documented), add `config/` to
   `.gitignore`.
2. Deploy; on restart entities get an availability topic and become available.
3. Rollback: move the file back to `config.yaml` and redeploy the previous version; saved
   files in `config/` are ignored by it.