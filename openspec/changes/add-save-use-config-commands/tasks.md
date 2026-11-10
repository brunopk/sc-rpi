# Tasks

## 1. Section state fixes

- [x] 1.1 Make `SectionsController._insert_section` store the given `is_on` in the ordered `_is_on` list, and make `turn_section_off` assign instead of insert.
  Verify with `test/controllers` tests that turn a section off and on, then check that:
  - `list_sections()` and `get_section()` agree
  - No other section changes
- [x] 1.2 Replace the overlap check in `_insert_section` with a strict inclusive-range check (`new_start <= existing_end and existing_start <= new_end`).
  Verify with controller tests that:
  - A shared boundary LED (10-20 then 20-30 and 5-10) raises `SECTION_OVERLAPPING`
  - An identical range (10-20) raises `SECTION_OVERLAPPING`
  - An enclosing range (5-25) raises `SECTION_OVERLAPPING`
  - Adjacent non-overlapping ranges (10-20 then 21-30) are still accepted
- [x] 1.3 Store each section's `name` in `SectionsController` and add `name` to `SectionInternalRepresentation`, returned by `get_section` and `list_sections`.
  Verify with a controller test that names from the config are returned.
- [x] 1.4 Apply each configured section's `color` and `is_on` in `_initialize_sections` instead of hardcoding `is_on=False`.
  Verify with a controller test using a config with an off section and a green section.

## 2. Config model, error codes and secret masking

- [x] 2.1 Add `description: str = ""` to `Config`.
  Verify that:
  - Loading `config_test.yaml` (no description) still works
  - A file with a description keeps it
- [x] 2.2 Add the error codes `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME`, `INVALID_CONFIG_NAME`, `MISSING_CONFIG_NAME`, `CONFIG_NOT_FOUND` and `INVALID_CONFIG` to `ErrorCode`.
  Verify that `map_exception` turns an `ApiError` with each code into a result with the status given in the specs.
- [x] 2.3 Implement `mask_secrets(config) -> Config` returning a copy with every secret value replaced by a placeholder. The secret values are listed in one place, `SECRET_PATHS` (today only the MQTT password).
  Verify with unit tests that:
  - The password is masked
  - The MQTT username and every other value are unchanged
  - The original `Config` is not modified
  - A distinctive value in every path of `SECRET_PATHS` appears nowhere in the masked output
- [x] 2.4 Rename `mqtt.broker_config` to `mqtt.broker` in the `Config` model, `config_test.yaml`, `config/default.example.yaml`, the code that reads it and `doc/configurations.md`.
  Verify that:
  - `grep -rn broker_config` has no matches outside `openspec/`
  - The config, masking and store tests pass

## 3. Config store

- [x] 3.1 Create `sc_rpi/utils/config/store.py` with `validate_name` (alphabet `[A-Za-z0-9_-]`, 1 to 64 characters, `MISSING_CONFIG_NAME` for a missing name, `INVALID_CONFIG_NAME` otherwise), `path_for` and `load`.
  Verify with unit tests for:
  - `../secret`, names with `/`, `.`, empty and over-long values
  - A valid name
  - Loading a missing name (`CONFIG_NOT_FOUND`)
  - Loading an unparsable file (`INVALID_CONFIG`)
- [x] 3.2 Implement `save(name, config, overwrite=False)` with a temporary file of mode `0600` in `config/`, given its final name with `os.link` (fails if the name is taken, mapped to `CONFIG_ALREADY_EXISTS`) or, with `overwrite=True`, with `Path.replace` (atomic swap). Reject `default` case-insensitively with `RESERVED_CONFIG_NAME` in `save` only, before anything else and in both modes. Always remove the temporary name.
  Verify with unit tests for:
  - A new name, with and without `overwrite`
  - An existing name without `overwrite` (`CONFIG_ALREADY_EXISTS`, file unchanged)
  - An existing name with `overwrite` (new content, mode `0600`)
  - `default` and `Default`, with and without `overwrite` (rejected on save, `default.yaml` unchanged, allowed on load)
  - File mode `0600`
  - No temporary file left after success or failure
- [x] 3.3 Verify that a config written by `save` and read by `load` is equal to the original, including section color, `is_on` and `description`.

## 4. Initial config location

- [x] 4.1 Read the initial configuration from `config/default.yaml` in `main.py` through the same loader used by the store.
  Verify that:
  - The app starts with a `config/default.yaml`
  - `test/command_test.py` still passes with `config_test.yaml`
- [x] 4.2 Move `config.yaml` to `config/default.example.yaml`, and add `config/` to `.gitignore` with an exception for `config/default.example.yaml`.
  Verify with `git status` and `git check-ignore -v config/default.yaml config/party.yaml config/default.example.yaml` that only the example is tracked.
- [x] 4.3 Update `README.md`, `CLAUDE.md` and `doc/configurations.md` to the new location and the copy step for a fresh clone.
  Verify with `grep -rn "config.yaml"` that no remaining mention refers to the old initial file (`config_test.yaml` and `openspec/config.yaml` are different files).

## 5. HardwareController and status result

- [x] 5.1 Extract the concatenation and the strip writing of `concatenate_sections` and `render` into private helpers `_concatenate_sections(sections, strip_length)` and `_render(colors)`, keeping both public methods unchanged.
  Verify that:
  - Existing command tests pass unchanged
  - `_concatenate_sections` on given sections returns the expected colors without touching the controller state
- [x] 5.2 Fix `_concatenate_sections` so the last section also honors `is_on` (today it is always rendered with its color when there are two or more sections).
  Verify with tests in `test_concatenating_sections.py` that:
  - An off last section is black with two or more sections
  - An off section in any position is black
- [x] 5.3 Keep the name of the active configuration in `HardwareController`: a private `_active_configuration` (`"default"` at startup, in memory only) read through `get_active_configuration()`, and the running description read through `get_description()`.
  Verify with controller tests that a new `HardwareController` (a restart) reports `default` and the description of the initial configuration.
- [x] 5.4 Add `HardwareController.prepare_config(loaded)`, returning the built sections as `list[SectionInternalRepresentation]` without changing any state, and `HardwareController.apply_prepared(sections, description, active_configuration)`, which renders from the given sections and only then replaces the sections, the description and the active configuration, following decision 4. `apply_prepared` is the only method that changes the active configuration.
  Verify with tests that:
  - `prepare_config` leaves the controller unchanged
  - A prepared valid config replaces sections, description and active configuration after `apply_prepared`
  - An overlapping config and a section beyond `strip_length` raise `INVALID_CONFIG` from `prepare_config` with state unchanged
  - A failing `render` makes `apply_prepared` raise and leaves sections, description and active configuration unchanged
- [x] 5.5 Add `HardwareController.get_current_config()` returning the initial `Config` with live sections and description. Only `save_config` uses it.
  Verify with a test that an `edit_section`, a `turn_section_off` and an applied config all show up in the returned `Config`.
- [x] 5.6 Make the status result payload (`StatusResultPayload`, built by `build_status_result` from `hw_controller`) contain the running sections, `active_configuration` and `description`.
  Verify that:
  - The `status` result reports `default` and an empty description at startup
  - It reports the loaded name and description after `use_config`
  - Tests that compare full result payloads pass

## 6. Home Assistant availability and refresh messages

- [x] 6.1 Add `SC_RPI_STATUS_TOPIC` (`scrpi/status`) and `build_ha_availability_topic` to `utils/topics.py`, and the optional `availability` (list of `{topic}`) and `availability_mode` fields to `HAMQTTDiscoveryMessage`.
  Verify with unit tests for:
  - The topics `scrpi/status` and `scrpi/homeassistant/<object_id>/availability`
  - The discovery JSON containing `availability_mode` `all` and both topics, global first
- [x] 6.2 Create `utils/homeassistant.py` with `build_ha_refresh_messages(previous_sections, new_sections, brightness)` returning the messages in the order `offline`, discovery (with the cross availability), `online`, state.
  Verify with unit tests for:
  - The order
  - The availability list and mode in each discovery message
  - No `offline` for ids present in both lists
  - No previous sections
  - ON/OFF, color and brightness in each state
- [x] 6.3 Make `Worker` publish the dict from `build_ha_refresh_messages` at startup in order, and remove `_publish_ha_entities`.
  Verify with a test (or a mocked MQTT client run) that startup publishes discovery with the availability list, `online` and state for each initial section.
- [x] 6.4 Publish the global availability, always retained, using the Paho client directly: `main.py` sets the LWT (`offline`) before `connect` and publishes `offline` (waiting for it) before `disconnect()`; `on_connect` publishes `online` on success, before subscribing.
  Verify with tests using a mocked client that:
  - `will_set` is called before `connect` with `scrpi/status`, `offline` and `retain=True`
  - `on_connect` publishes `online` retained on success and nothing on failure
  - The shutdown `offline` is published before `disconnect`
- [x] 6.5 Update `doc/homeassistant.md` for the global topic, the cross availability, the LWT, birth and shutdown messages, the per-entity `offline` and `online` messages, and which topics are retained.
  Check that the documented topics match `topics.py`.

## 7. `use_config` and `reset` (using the `apply_named_config` helper for both)

- [x] 7.1 Implement `apply_named_config(hw_controller, command_name, config_name, brightness)` in `utils/commands/` following decisions 5 and 6: validate the name, load, read previous sections, `prepare_config`, build the result from the previous and prepared sections with the SC RPi status entry first and the Home Assistant messages after, and call `apply_prepared` (with `config_name` as the new active configuration) as the last step.
  Verify with a unit test, built without a command instance, that:
  - The result keys and their order match the specs
  - The payload lists each section's id, start, end, color and `is_on`, the new active configuration and the description
  - A failure while building the result leaves the controller and the strip unchanged
- [x] 7.2 Add the `use_config` command (`commands/use_config/` with `args.py` and `command.py`, `name` required), with a comment inside `run()` explaining why it uses `prepare_config` and `apply_prepared` instead of mutate-then-render.
  Verify with `test/commands/test_use_config_cmd.py` for:
  - Switching configs, and the description loaded
  - The loaded name becoming the active configuration
  - A failed load (`CONFIG_NOT_FOUND`, `INVALID_CONFIG`, `INVALID_CONFIG_NAME`) leaving the active name unchanged
  - Previous entities marked unavailable
  - `MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME` and `CONFIG_NOT_FOUND`
  - `INVALID_CONFIG` (unreadable file and a section beyond the strip length) with state unchanged
  - No file changed in `config/`
  - MQTT settings not applied
  - The result `payload` equal to the `payload` of a `status` command received right after
- [x] 7.3 Add the `reset` command (`commands/reset/`, optional `name`), which applies `name` like `use_config` or, when omitted, reloads the active configuration, with a comment inside `run()` explaining why it uses `prepare_config` and `apply_prepared`.
  Verify with `test/commands/test_reset_cmd.py` for:
  - Reset without a name at startup (`default`)
  - Reset without a name after `use_config night` and some edits (restores `night`)
  - Reset with a saved name, which becomes the active configuration
  - Reset with an unknown name
  - Reset without a name when the active file is missing or invalid (error, state and active name unchanged)
  - A section configured off
  - Previous entities marked unavailable
  - No file changed in `config/` (with and without a name)
  - The result `payload` equal to the `payload` of a `status` command received right after
- [x] 7.4 Document `use_config` and `reset`, with arguments, results and error codes, in `doc/commands.md`, including that the active configuration is not persisted and starts as `default` (also in `doc/configurations.md`).
  Check that each documented example matches the output of the corresponding test.

## 8. `get_config`

- [x] 8.1 Add the `get_config` command (`name` required) returning `mask_secrets(store.load(name))` as its payload (the `Config` structure) without applying it, and delete the separate result models under `commands/get_config/result/`. A missing `name` fails with 400 `MISSING_CONFIG_NAME`.
  Verify with `test/commands/test_get_config_cmd.py` that it checks:
  - The `mqtt` and `strip` keys, `mqtt.broker` host and port, `color` and `is_on` per section, and `description`
  - The masked password
  - `CONFIG_NOT_FOUND`, `INVALID_CONFIG_NAME` and `MISSING_CONFIG_NAME`
  - An unchanged strip, running sections and active configuration, and no file changed in `config/`
  - The command calls neither `prepare_config` nor `apply_prepared`
  - `grep -rn "get_config.result" src test` returns no matches
  - `get_current_config()` is used only by `save_config`
- [x] 8.2 Document `get_config` in `doc/commands.md`, with its required `name`, the error codes and the payload keys (`mqtt` and `strip`).
  Check that the documented example matches the test output.

## 9. `save_config`

- [x] 9.1 Add the `save_config` command (`commands/save_config/`) with optional `name` (the active configuration's name when omitted, as if it had been given), `description` and boolean `overwrite` (default `False`). It builds the file's `Config` from `get_current_config()` (sections keep their ids and names), saves it through `store.save` and returns that masked `Config` as its payload, exactly the same as the `get_config` payload for that configuration, with no Home Assistant entries and without changing the active configuration.
  Verify with `test/commands/test_save_config_cmd.py` for:
  - A new save (status 202, payload with the `Config` structure)
  - Ids and names kept
  - Strip and running sections unchanged
  - No Home Assistant message
  - Description saved and omitted
  - Masked password in the result while the file keeps the real one
  - `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME` (including `Default` and `DEFAULT`, with `default.yaml` unchanged) and `INVALID_CONFIG_NAME`
  - `overwrite` true on an existing name (status 202, file updated, strip and Home Assistant untouched), on a new name, and with `default` (`RESERVED_CONFIG_NAME`)
  - `overwrite` false or omitted on an existing name (`CONFIG_ALREADY_EXISTS`)
  - Name omitted with `overwrite` true (the active file is updated, status 202)
  - Name omitted with `overwrite` false or omitted (`CONFIG_ALREADY_EXISTS`, file unchanged)
  - Name omitted while `default` is active, with and without `overwrite` (`RESERVED_CONFIG_NAME`, `default.yaml` unchanged)
  - A save, named or not, leaving the active name unchanged
- [x] 9.2 Verify the round trips:
  - A section that is off with color `[0, 255, 0]` is reported as off and green after `save_config` then `get_config` with the same name
  - The `get_config` result payload equals the `save_config` result payload
- [x] 9.3 Document `save_config` in `doc/commands.md` (the optional `name` and its omitted-name cases, `overwrite`, the result, error codes, and that `default` is reserved), and in `doc/configurations.md` (an existing saved configuration is only replaced with `overwrite`).
  Check that each documented example matches the test output.

## 10. Integration checks

- [x] 10.1 Add a `test_result_ignores_initial_config` test (the steps are in `CLAUDE.md`; see also Risks in `design.md`) to `turn_section_on`, `turn_section_off`, `edit_section`, `status` and `save_config`.
  Verify that the `status` test also checks `active_configuration` and `description`.
- [x] 10.2 Verify that:
  - `help` lists `save_config` and `use_config`
  - `doc/commands.md` and `doc/homeassistant.md` cover every new or changed command and error code from the specs
- [x] 10.3 Run `python -m unittest discover` from the repository root and `ruff check` on the files added or changed by this change, and verify that both pass (the existing repository-wide ruff errors are out of scope and left for a separate change; the only remaining errors in the new files are the `TODO` rules for a TODO that already existed).

## 11. Project guidelines

- [x] 11.1 Update `CLAUDE.md`.
  Check that:
  - The "Command pattern" section states that results must be built from `hw_controller` (`list_sections()` or `get_current_config()`), never from `config.strip.sections`
  - The "Tests" section requires a `test_result_ignores_initial_config` test (as described in 10.1) for every command whose result shows the running sections
  - The terminology lists the **active configuration** (the name `reset` reloads, `default` at startup, in memory only)
  - The "Code" section requires private instance state (`_name`) read through `get_<name>()` methods
