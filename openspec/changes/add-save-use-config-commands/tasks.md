# Tasks

## 1. Section state fixes

- [x] 1.1 Make `SectionsController._insert_section` store the given `is_on` in the ordered `_is_on` list and make `turn_section_off` assign instead of insert; verify with `test/controllers` tests that turn a section off and on and then check that `list_sections()` and `get_section()` agree and no other section changes.
- [x] 1.2 Replace the overlap check in `_insert_section` with a strict inclusive-range check (`new_start <= existing_end and existing_start <= new_end`); verify with controller tests for a shared boundary LED (10-20 then 20-30 and 5-10), an identical range (10-20) and an enclosing range (5-25), all raising `SECTION_OVERLAPPING`, while adjacent non-overlapping ranges (10-20 then 21-30) are still accepted.
- [x] 1.3 Store each section's `name` in `SectionsController` and add `name` to `SectionInternalRepresentation`, returned by `get_section` and `list_sections`; verify with a controller test that names from the config are returned.
- [x] 1.4 Apply each configured section's `color` and `is_on` in `_initialize_sections` instead of hardcoding `is_on=False`; verify with a controller test using a config with an off section and a green section.

## 2. Config model, error codes and secret masking

- [x] 2.1 Add `description: str = ""` to `Config` and verify that loading `config_test.yaml` (no description) still works and a file with a description keeps it.
- [x] 2.2 Add the error codes `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME`, `INVALID_CONFIG_NAME`, `MISSING_CONFIG_NAME`, `CONFIG_NOT_FOUND` and `INVALID_CONFIG` to `ErrorCode`; verify that `map_exception` turns an `ApiError` with each code into a result with the status given in the specs.
- [x] 2.3 Implement `mask_secrets(config) -> Config` returning a copy with the MQTT password replaced by a placeholder; verify with a unit test that the password is masked, the MQTT username and every other value are unchanged, and the original `Config` is not modified.

## 3. Config store

- [x] 3.1 Create `sc_rpi/utils/config/store.py` with `validate_name` (alphabet `[A-Za-z0-9_-]`, 1 to 64 characters, `MISSING_CONFIG_NAME` for a missing name, `INVALID_CONFIG_NAME` otherwise), `path_for` and `load`; verify with unit tests for `../secret`, names with `/`, `.`, empty and over-long values, a valid name, loading a missing name (`CONFIG_NOT_FOUND`) and loading an unparsable file (`INVALID_CONFIG`).
- [x] 3.2 Implement `save(name, config)` with a temporary file of mode `0600` in `config/`, `os.link` to the final name and removal of the temporary name; reject `default` case-insensitively with `RESERVED_CONFIG_NAME` in `save` only, and map `FileExistsError` to `CONFIG_ALREADY_EXISTS`; verify with unit tests for a new name, an existing name (file unchanged), `default` and `Default` (rejected on save, allowed on load), file mode `0600`, and no temporary file left after success or failure.
- [x] 3.3 Verify that a config written by `save` and read by `load` is equal to the original, including section color, `is_on` and `description`.

## 4. Boot config location

- [x] 4.1 Read the boot configuration from `config/default.yaml` in `main.py` through the same loader used by the store; verify that the app starts with a `config/default.yaml` and that `test/command_test.py` still passes with `config_test.yaml`.
- [x] 4.2 Move `config.yaml` to `config/default.example.yaml`, add `config/` to `.gitignore` with an exception for `config/default.example.yaml`, and verify with `git status` and `git check-ignore -v config/default.yaml config/party.yaml config/default.example.yaml` that only the example is tracked.
- [x] 4.3 Update `README.md`, `CLAUDE.md` and `doc/configurations.md` to the new location and the copy step for a fresh clone; verify with `grep -rn "config.yaml"` that no remaining mention refers to the old boot file (`config_test.yaml` and `openspec/config.yaml` are different files).

## 5. HardwareController configuration methods

- [ ] 5.1 Let `concatenate_sections` and `render` take an optional `sections` argument, defaulting to the live sections; verify that existing command tests pass unchanged and a new test renders given sections without changing the controller state.
- [ ] 5.2 Add `HardwareController.prepare_config(loaded)` returning the built sections as `list[SectionInternalRepresentation]` (no state change) and `HardwareController.apply_prepared(sections, description)` (render from the given sections, then replace the sections in `SectionsController` and the description), following decision 4; verify with tests that `prepare_config` leaves the controller unchanged, a prepared valid config replaces sections and description after `apply_prepared`, an overlapping config and a section beyond `strip_length` raise `INVALID_CONFIG` from `prepare_config` with state unchanged, and a failing `render` makes `apply_prepared` raise and leaves sections and description unchanged.
- [ ] 5.3 Add `HardwareController.get_current_config()` returning the boot `Config` with live sections and description; verify with a test that an `edit_section`, a `turn_section_off` and an applied config all show up in the returned `Config`.

## 6. Home Assistant availability and refresh messages

- [ ] 6.1 Add `build_ha_availability_topic` to `utils/topic_utils.py` and the optional `availability_topic` field to `HAMQTTDiscoveryMessage`; verify with unit tests for the topic `scrpi/homeassistant/<object_id>/availability` and for the discovery JSON containing `availability_topic`.
- [ ] 6.2 Create `utils/homeassistant.py` with `build_ha_refresh_messages(previous_sections, new_sections, brightness)` returning the messages in the order `offline`, discovery, `online`, state; verify with unit tests for the order, no `offline` for ids present in both lists, no previous sections, and ON/OFF, color and brightness in each state.
- [ ] 6.3 Make `Worker` publish the dict from `build_ha_refresh_messages` at startup in order and remove `_publish_ha_entities`; verify with a test (or a mocked MQTT client run) that startup publishes discovery with the availability topic, `online` and state for each boot section.
- [ ] 6.4 Update `doc/homeassistant.md` for availability, the `offline` and `online` messages, and the section id change when loading another config; verify that the documented topic matches `build_ha_availability_topic`.

## 7. Shared apply, `use_config` and `reset`

- [ ] 7.1 Implement `apply_named_config(hw_controller, command_name, config_name, brightness)` in `utils/commands/` following decisions 5 and 6: validate the name, load, read previous sections, `prepare_config`, build the result from the previous and prepared sections with the SC RPi status entry first and the Home Assistant messages after, and call `apply_prepared` as the last step; verify with a unit test, built without a command instance, that the result keys and their order match the specs the payload lists each section's id, start, end, color and `is_on`, and a failure while building the result leaves the controller and the strip unchanged.
- [ ] 7.2 Add the `use_config` command (`commands/use_config/` with `args.py` and `command.py`, `name` required), with a class docstring explaining why it uses `prepare_config` and `apply_prepared` instead of mutate-then-render, and verify with `test/commands/test_use_config_cmd.py` for switching configs, description loaded, previous entities marked unavailable, `MISSING_CONFIG_NAME`, `INVALID_CONFIG_NAME`, `CONFIG_NOT_FOUND`, `INVALID_CONFIG` (unreadable file and a section beyond the strip length) with state unchanged, no file changed in `config/`, and MQTT settings not applied.
- [ ] 7.3 Make `Reset` accept an optional `name` and call `apply_named_config` with `"default"` when omitted, removing the rollback TODO and documenting in the class docstring why it uses `prepare_config` and `apply_prepared`; verify by updating `test/commands/test_reset_cmd.py` for reset without a name, with a saved name, with an unknown name, a section configured off, previous entities marked unavailable, and results identical to `use_config` except for `command_name`.
- [ ] 7.4 Document `use_config` and the changed `reset`, with arguments, results and error codes, in `doc/commands.md`; verify that each documented example matches the output of the corresponding test.

## 8. `get_config`

- [ ] 8.1 Return `mask_secrets(hw_controller.get_current_config())` as the `get_config` payload and delete the separate result models under `commands/get_config/result/`; verify by updating `test/commands/test_get_config_cmd.py` for `mqtt` and `strip` keys, `color` and `is_on` per section, `description`, broker host and port, the masked password, and a result reflecting an earlier `edit_section`.
- [ ] 8.2 Add the optional `name` argument that returns the masked saved config through `store.load` without applying it; verify with tests for an existing name, `CONFIG_NOT_FOUND`, `INVALID_CONFIG_NAME` and an unchanged strip.
- [ ] 8.3 Document the new `get_config` argument and the breaking payload keys in `doc/commands.md`; verify that the documented example matches the test output.

## 9. `save_config`

- [ ] 9.1 Add the `save_config` command (`commands/save_config/`, `name` required, `description` optional) that builds the file's `Config` from `get_current_config()`, rewrites section ids to `<name>_section_<n>` ordered by `start` on that copy, saves it through `store.save` and returns `{"name", "config"}` with masked secrets and no Home Assistant entries; verify with `test/commands/test_save_config_cmd.py` for a new save, ids prefixed and names kept, saving again under another name (no `party_` prefix), running sections keeping their ids, no Home Assistant message, description saved and omitted, masked password in the result while the file keeps the real one, `CONFIG_ALREADY_EXISTS`, `RESERVED_CONFIG_NAME`, `INVALID_CONFIG_NAME` and `MISSING_CONFIG_NAME`.
- [ ] 9.2 Verify the round trips: a section that is off with color `[0, 255, 0]` is reported as off and green after `save_config` then `get_config` with the same name, and the `get_config` result equals the `save_config` result's `config`.
- [ ] 9.3 Document `save_config`, its arguments, result and error codes in `doc/commands.md`; verify that the documented example matches the test output.

## 10. Integration checks

- [ ] 10.1 Run `ruff check .` and `python -m unittest discover` from the repository root and verify that both pass.
- [ ] 10.2 Verify that `help` lists `save_config` and `use_config`, and that `doc/commands.md` and `doc/homeassistant.md` cover every new or changed command and error code from the specs.