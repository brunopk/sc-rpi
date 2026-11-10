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
- [x] 2.3 Implement `mask_secrets(config) -> Config` returning a copy with the MQTT password replaced by a placeholder.
  Verify with a unit test that:
  - The password is masked
  - The MQTT username and every other value are unchanged
  - The original `Config` is not modified
- [x] 2.4 Test `mask_secrets` for every secret field, not only the MQTT password.
  Verify with a unit test that fills each field in the secret list with a distinctive value and checks that none of those values appears anywhere in the masked output, so adding a secret to the list is enough to mask it in `get_config` and `save_config`.
- [x] 2.5 Rename `mqtt.broker_config` to `mqtt.broker` in the `Config` model, `config_test.yaml`, `config/default.example.yaml`, the code that reads it and `doc/configurations.md`.
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
- [x] 3.2 Implement `save(name, config)` with a temporary file of mode `0600` in `config/`, `os.link` to the final name and removal of the temporary name. Reject `default` case-insensitively with `RESERVED_CONFIG_NAME` in `save` only, and map `FileExistsError` to `CONFIG_ALREADY_EXISTS`.
  Verify with unit tests for:
  - A new name
  - An existing name (file unchanged)
  - `default` and `Default` (rejected on save, allowed on load)
  - File mode `0600`
  - No temporary file left after success or failure
- [x] 3.3 Add `overwrite: bool = False` to `store.save`: with `True`, give the temporary file its final name with `os.replace` instead of `os.link`; the reserved name check stays first and applies in both modes.
  Verify with unit tests for:
  - Overwriting an existing name (new content, mode `0600`)
  - `overwrite=False` on an existing name (`CONFIG_ALREADY_EXISTS`, file unchanged)
  - `overwrite=True` on a new name
  - `default` and `Default` with `overwrite=True` (`RESERVED_CONFIG_NAME`, `default.yaml` unchanged)
  - No temporary file left after success or failure
- [x] 3.4 Verify that a config written by `save` and read by `load` is equal to the original, including section color, `is_on` and `description`.

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
- [x] 5.3 Add `HardwareController.prepare_config(loaded)` returning the built sections as `list[SectionInternalRepresentation]` (no state change), and `HardwareController.apply_prepared(sections, description)` (render from the given sections, then replace the sections in `SectionsController` and the description), following decision 4.
  Verify with tests that:
  - `prepare_config` leaves the controller unchanged
  - A prepared valid config replaces sections and description after `apply_prepared`
  - An overlapping config and a section beyond `strip_length` raise `INVALID_CONFIG` from `prepare_config` with state unchanged
  - A failing `render` makes `apply_prepared` raise and leaves sections and description unchanged
- [x] 5.4 Add `HardwareController.get_current_config()` returning the initial `Config` with live sections and description. Only `save_config` uses it.
  Verify with a test that an `edit_section`, a `turn_section_off` and an applied config all show up in the returned `Config`.
- [x] 5.5 Add `active_configuration: str` (initial value `"default"`) to `HardwareController` and a third argument, `active_configuration`, to `apply_prepared`, which replaces it together with the sections and the description after a successful render.
  Verify with controller tests that:
  - A new `HardwareController` (a restart) reports `default`
  - `apply_prepared` sets the given name
  - A failing `render` leaves the active name unchanged
- [x] 5.6 Add `active_configuration` and `description` to `StatusResultPayload`, filled by `build_status_result` from `hw_controller`.
  Verify that:
  - The `status` result reports `default` and an empty description at startup
  - It reports the loaded name and description after `use_config`
  - Existing tests that compare full result payloads still pass

## 6. Home Assistant availability and refresh messages

- [x] 6.1 Add `build_ha_availability_topic` to `utils/topics.py` and the optional `availability_topic` field to `HAMQTTDiscoveryMessage`.
  Verify with unit tests for:
  - The topic `scrpi/homeassistant/<object_id>/availability`
  - The discovery JSON containing `availability_topic`
- [x] 6.2 Create `utils/homeassistant.py` with `build_ha_refresh_messages(previous_sections, new_sections, brightness)` returning the messages in the order `offline`, discovery, `online`, state.
  Verify with unit tests for:
  - The order
  - No `offline` for ids present in both lists
  - No previous sections
  - ON/OFF, color and brightness in each state
- [x] 6.3 Make `Worker` publish the dict from `build_ha_refresh_messages` at startup in order, and remove `_publish_ha_entities`.
  Verify with a test (or a mocked MQTT client run) that startup publishes discovery with the availability topic, `online` and state for each initial section.
- [x] 6.4 Update `doc/homeassistant.md` for availability and the `offline` and `online` messages.
  Check that the documented topic matches `build_ha_availability_topic`.

## 7. `use_config` and `reset` (using the new `apply_named_config` helper for both)

- [x] 7.1 Implement `apply_named_config(hw_controller, command_name, config_name, brightness)` in `utils/commands/` following decisions 5 and 6: validate the name, load, read previous sections, `prepare_config`, build the result from the previous and prepared sections with the SC RPi status entry first and the Home Assistant messages after, and call `apply_prepared` as the last step.
  Verify with a unit test, built without a command instance, that:
  - The result keys and their order match the specs
  - The payload lists each section's id, start, end, color and `is_on`
  - A failure while building the result leaves the controller and the strip unchanged
- [x] 7.2 Add the `use_config` command (`commands/use_config/` with `args.py` and `command.py`, `name` required), with a comment inside `run()` explaining why it uses `prepare_config` and `apply_prepared` instead of mutate-then-render.
  Verify with `test/commands/test_use_config_cmd.py` for:
  - Switching configs
  - Description loaded
  - Previous entities marked unavailable
  - `MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME` and `CONFIG_NOT_FOUND`
  - `INVALID_CONFIG` (unreadable file and a section beyond the strip length) with state unchanged
  - No file changed in `config/`
  - MQTT settings not applied
- [x] 7.3 Make `Reset` accept an optional `name` and call `apply_named_config` with `"default"` when omitted, removing the rollback TODO and documenting in a comment inside `run()` why it uses `prepare_config` and `apply_prepared`.
  Verify by updating `test/commands/test_reset_cmd.py` for:
  - Reset without a name
  - Reset with a saved name
  - Reset with an unknown name
  - A section configured off
  - Previous entities marked unavailable
  - No file changed in `config/` (with and without a name)
- [x] 7.4 Make both commands maintain the active configuration: `apply_named_config` passes `config_name` to `apply_prepared`, and `Reset` passes `hw_controller.active_configuration` instead of `"default"` when `name` is omitted.
  Verify with command tests for:
  - `use_config` and `reset` with a name make that name active
  - A failed load (`CONFIG_NOT_FOUND`, `INVALID_CONFIG`, a render failure) leaves the active name unchanged
  - `reset` without a name after `use_config night` and some edits restores `night`
  - `reset` without a name when the active file is missing or invalid fails, with the state and the active name unchanged
  - `use_config` and `reset` results have the same `payload` as a `status` command received right after
- [x] 7.5 Document `use_config` and the changed `reset`, with arguments, results and error codes, in `doc/commands.md`, including that the active configuration is not persisted and starts as `default` (also in `doc/configurations.md`).
  Check that each documented example matches the output of the corresponding test.

## 8. `get_config`

- [x] 8.1 Make `get_config` return a masked `Config` as its payload (`mask_secrets`), and delete the separate result models under `commands/get_config/result/`.
  Verify that:
  - `grep -rn "get_config.result" src test` returns no matches
  - `ruff check src/sc_rpi/commands/get_config` passes
- [x] 8.2 Make `name` required in `get_config`: it always returns `mask_secrets(store.load(name))` without applying it, and a missing `name` fails with 400 `MISSING_CONFIG_NAME`. Remove the running-configuration form and its tests (including the `edit_section` check and its `test_result_ignores_initial_config`).
  Verify with `test/commands/test_get_config_cmd.py` that it checks:
  - The `mqtt` and `strip` keys, `mqtt.broker` host and port, `color` and `is_on` per section, and `description`
  - The masked password
  - `CONFIG_NOT_FOUND`, `INVALID_CONFIG_NAME` and `MISSING_CONFIG_NAME`
  - An unchanged strip and running sections, and no file changed in `config/`
  - The command calls neither `prepare_config` nor `apply_prepared`
  - `get_current_config()` is used only by `save_config`
- [x] 8.3 Document `get_config` with its required `name`, the 400 for a missing one and the breaking payload keys in `doc/commands.md`.
  Check that the documented example matches the test output.

## 9. `save_config`

- [x] 9.1 Add the `save_config` command (`commands/save_config/`, `description` optional) that builds the file's `Config` from `get_current_config()` (sections keep their ids and names), saves it through `store.save` and returns the result with masked secrets and no Home Assistant entries.
  Verify with `test/commands/test_save_config_cmd.py` for:
  - A new save
  - Ids and names kept
  - Strip and running sections unchanged
  - No Home Assistant message
  - Description saved and omitted
  - Masked password in the result while the file keeps the real one
  - `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME` (including `Default` and `DEFAULT`, with `default.yaml` unchanged) and `INVALID_CONFIG_NAME`
- [x] 9.2 Make the `save_config` payload the masked `Config` it saved, exactly the same as the `get_config` payload for that configuration.
  Verify with `test/commands/test_save_config_cmd.py` that:
  - The payload has the `Config` structure (`mqtt`, `strip`, `description`)
  - The `get_config` result payload for the same name equals the `save_config` result payload
- [x] 9.3 Add the optional boolean `overwrite` (default `False`) to the `save_config` args and pass it to `store.save`.
  Verify with `test/commands/test_save_config_cmd.py` for:
  - Overwrite of an existing name (status 202, file updated, strip and Home Assistant untouched)
  - `overwrite` false or omitted on an existing name (`CONFIG_ALREADY_EXISTS`)
  - `overwrite` true with `default` (`RESERVED_CONFIG_NAME`)
- [x] 9.4 Make `name` optional in `save_config`: when omitted, use `hw_controller.active_configuration` and continue as if it had been given (so `overwrite`, the reserved name check and name validation apply unchanged). `save_config` never changes the active configuration.
  Verify with `test/commands/test_save_config_cmd.py` for:
  - Name omitted with `overwrite` true (the active file is updated, the active name is unchanged, status 202)
  - Name omitted with `overwrite` false or omitted (`CONFIG_ALREADY_EXISTS`, file unchanged)
  - Name omitted while `default` is active, with and without `overwrite` (`RESERVED_CONFIG_NAME`, `default.yaml` unchanged)
  - A named save does not change the active name
- [x] 9.5 Verify the round trip: a section that is off with color `[0, 255, 0]` is reported as off and green after `save_config` then `get_config` with the same name.
- [x] 9.6 Document `save_config` in `doc/commands.md` (the optional `name` and its three omitted-name cases, `overwrite`, the flat result, error codes, and that `default` is reserved), and `overwrite` in `doc/configurations.md`, replacing the statement that an existing saved configuration is never overwritten.
  Check that each documented example matches the test output.

## 10. Integration checks

- [x] 10.1 Add `test_result_ignores_initial_config` tests (see Risks in `design.md`) for `turn_section_on`, `turn_section_off` and `edit_section`.
  Verify with, for each command:
  - The initial configuration (`hw_controller._config`) of section B is tampered with, and the tampered value differs from the live one
  - The command runs on section A
  - The result shows the command's change for A and the live values for B, never the tampered ones
- [x] 10.2 Add `test_result_ignores_initial_config` tests for `status` and `save_config`.
  Verify with, for each command:
  - Section A is changed by an earlier command, such as `edit_section`
  - The initial configuration (`hw_controller._config`) of section B is tampered with, and the tampered value differs from the live one
  - The command runs
  - The result shows the change for A and the live values for B, never the tampered ones
  - The `status` result also reports `active_configuration` and `description`
- [x] 10.3 Verify that:
  - `help` lists `save_config` and `use_config`
  - `doc/commands.md` and `doc/homeassistant.md` cover every new or changed command and error code from the specs
- [x] 10.4 Run `python -m unittest discover` from the repository root and `ruff check` on the files added or changed by this change, and verify that both pass (the existing repository-wide ruff errors are out of scope and left for a separate change; the only remaining errors in the new files are the `TODO` rules for a TODO that already existed).

## 11. Project guidelines

- [x] 11.1 Update `CLAUDE.md`.
  Check that:
  - The "Command pattern" section states that results must be built from `hw_controller` (`list_sections()` or `get_current_config()`), never from `config.strip.sections`
  - The "Tests" section requires a `test_result_ignores_initial_config` test (as described in 10.1 and 10.2) for every command whose result includes sections
- [x] 11.2 Update the `CLAUDE.md` terminology with the **active configuration** (the name `reset` reloads, `default` at startup, in memory only), and make sure its test guidance no longer asks for a `test_result_ignores_initial_config` test for `get_config`.