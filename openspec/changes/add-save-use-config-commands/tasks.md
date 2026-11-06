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
- [x] 3.2 Implement `save(name, config)` with a temporary file of mode `0600` in `config/`, `os.link` to the final name and removal of the temporary name. Reject `default` case-insensitively with `RESERVED_CONFIG_NAME` in `save` only, and map `FileExistsError` to `CONFIG_ALREADY_EXISTS`.
  Verify with unit tests for:
  - A new name
  - An existing name (file unchanged)
  - `default` and `Default` (rejected on save, allowed on load)
  - File mode `0600`
  - No temporary file left after success or failure
- [x] 3.3 Verify that a config written by `save` and read by `load` is equal to the original, including section color, `is_on` and `description`.

## 4. Boot config location

- [x] 4.1 Read the boot configuration from `config/default.yaml` in `main.py` through the same loader used by the store.
  Verify that:
  - The app starts with a `config/default.yaml`
  - `test/command_test.py` still passes with `config_test.yaml`
- [x] 4.2 Move `config.yaml` to `config/default.example.yaml`, and add `config/` to `.gitignore` with an exception for `config/default.example.yaml`.
  Verify with `git status` and `git check-ignore -v config/default.yaml config/party.yaml config/default.example.yaml` that only the example is tracked.
- [x] 4.3 Update `README.md`, `CLAUDE.md` and `doc/configurations.md` to the new location and the copy step for a fresh clone.
  Verify with `grep -rn "config.yaml"` that no remaining mention refers to the old boot file (`config_test.yaml` and `openspec/config.yaml` are different files).

## 5. HardwareController configuration methods

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
- [x] 5.4 Add `HardwareController.get_current_config()` returning the boot `Config` with live sections and description.
  Verify with a test that an `edit_section`, a `turn_section_off` and an applied config all show up in the returned `Config`.

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
  Verify with a test (or a mocked MQTT client run) that startup publishes discovery with the availability topic, `online` and state for each boot section.
- [x] 6.4 Update `doc/homeassistant.md` for availability, the `offline` and `online` messages, and the section id change when loading another config.
  Verify that the documented topic matches `build_ha_availability_topic`.

## 7. Shared apply, `use_config` and `reset`

- [ ] 7.1 Implement `apply_named_config(hw_controller, command_name, config_name, brightness)` in `utils/commands/` following decisions 5 and 6: validate the name, load, read previous sections, `prepare_config`, build the result from the previous and prepared sections with the SC RPi status entry first and the Home Assistant messages after, and call `apply_prepared` as the last step.
  Verify with a unit test, built without a command instance, that:
  - The result keys and their order match the specs
  - The payload lists each section's id, start, end, color and `is_on`
  - A failure while building the result leaves the controller and the strip unchanged
- [ ] 7.2 Add the `use_config` command (`commands/use_config/` with `args.py` and `command.py`, `name` required), with a class docstring explaining why it uses `prepare_config` and `apply_prepared` instead of mutate-then-render.
  Verify with `test/commands/test_use_config_cmd.py` for:
  - Switching configs
  - Description loaded
  - Previous entities marked unavailable
  - `MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME` and `CONFIG_NOT_FOUND`
  - `INVALID_CONFIG` (unreadable file and a section beyond the strip length) with state unchanged
  - No file changed in `config/`
  - MQTT settings not applied
- [ ] 7.3 Make `Reset` accept an optional `name` and call `apply_named_config` with `"default"` when omitted, removing the rollback TODO and documenting in the class docstring why it uses `prepare_config` and `apply_prepared`.
  Verify by updating `test/commands/test_reset_cmd.py` for:
  - Reset without a name
  - Reset with a saved name
  - Reset with an unknown name
  - A section configured off
  - Previous entities marked unavailable
  - Results identical to `use_config` except for `command_name`
- [ ] 7.4 Document `use_config` and the changed `reset`, with arguments, results and error codes, in `doc/commands.md`.
  Verify that each documented example matches the output of the corresponding test.

## 8. `get_config`

- [ ] 8.1 Make `get_config` return `mask_secrets(hw_controller.get_current_config())` as its payload, and delete the separate result models under `commands/get_config/result/`.
  Verify that:
  - `grep -rn "get_config.result" src test` returns no matches
  - `ruff check src/sc_rpi/commands/get_config` passes
- [ ] 8.2 Update `test/commands/test_get_config_cmd.py` for the new payload.
  Verify that it checks:
  - The `mqtt` and `strip` keys
  - `mqtt.broker` host and port
  - The masked password
  - `color` and `is_on` per section
  - `description`
  - That after an `edit_section` the result shows the edited section (not the boot values)
- [ ] 8.3 Add the optional `name` argument to `get_config`: when present, return the masked config saved under that name (loaded with `store.load`) without applying it.
  Verify that:
  - `ruff check src/sc_rpi/commands/get_config` passes
  - The command calls neither `prepare_config` nor `apply_prepared`
- [ ] 8.4 Add tests for `get_config` with `name` in `test/commands/test_get_config_cmd.py`.
  Verify that they cover:
  - An existing name (config returned, password masked)
  - `CONFIG_NOT_FOUND`
  - `INVALID_CONFIG_NAME`
  - An unchanged strip and running sections
- [ ] 8.5 Document the new `get_config` argument and the breaking payload keys in `doc/commands.md`.
  Verify that the documented example matches the test output.

## 9. `save_config`

- [ ] 9.1 Add the `save_config` command (`commands/save_config/`, `name` required, `description` optional) that builds the file's `Config` from `get_current_config()`, rewrites section ids to `<name>_section_<n>` ordered by `start` on that copy, saves it through `store.save` and returns `{"name", "config"}` with masked secrets and no Home Assistant entries.
  Verify with `test/commands/test_save_config_cmd.py` for:
  - A new save
  - Ids prefixed and names kept
  - Saving again under another name (no `party_` prefix)
  - Running sections keeping their ids
  - No Home Assistant message
  - Description saved and omitted
  - Masked password in the result while the file keeps the real one
  - `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME`, `INVALID_CONFIG_NAME` and `MISSING_CONFIG_NAME`
- [ ] 9.2 Verify the round trips:
  - A section that is off with color `[0, 255, 0]` is reported as off and green after `save_config` then `get_config` with the same name
  - The `get_config` result equals the `save_config` result's `config`
- [ ] 9.3 Document `save_config`, its arguments, result and error codes in `doc/commands.md`.
  Verify that the documented example matches the test output.

## 10. Integration checks

- [ ] 10.1 Run `ruff check .` and `python -m unittest discover` from the repository root and verify that both pass.
- [ ] 10.2 Verify that:
  - `help` lists `save_config` and `use_config`
  - `doc/commands.md` and `doc/homeassistant.md` cover every new or changed command and error code from the specs