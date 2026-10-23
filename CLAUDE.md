# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

SC RPi controls a WS2812B LED strip attached to a Raspberry Pi. It runs as an MQTT
client/server: it receives JSON commands over MQTT (either directly, via SC RPi's own
topic, or translated from Home Assistant light entity commands) and drives the strip
hardware in response.

## Commands

```bash
# Install dependencies
uv sync --group dev          # development (uses mocked GPIO/ws281x libs from /lib)
uv sync --group rpi          # on an actual Raspberry Pi (real hardware libs)

# Run the app (reads config.yaml from CWD)
source .venv/bin/activate
python -m sc_rpi.main

# Lint
ruff check .
ruff check file.py --fix

# Tests (must be run from repo root; uses config_test.yaml)
python -m unittest discover
python -m unittest test.commands.test_turn_section_on_cmd   # single module
python -m unittest test.commands.test_turn_section_on_cmd.TestTurnSectionOnCmd.test_x  # single test
```

On non-Raspberry-Pi systems (e.g. macOS dev), `rpi-ws281x` and `RPi.GPIO` are unavailable;
the `dev` dependency group substitutes editable mock packages from `lib/rpi-ws281x-mock`
and `lib/rpi-gpio-mock` instead, so the whole app runs and tests pass without real hardware.

## Architecture

### Command pattern + dynamic discriminated dispatch

Every API operation (`turn_section_on`, `turn_section_off`, `edit_section`, `get_config`,
`help`, `reset`, `status`, `version`) lives in its own subpackage under
`src/sc_rpi/commands/<name>/` with a `command.py` (the `Command` subclass) and usually an
`args.py` (its typed argument dataclass). All commands subclass `Command`
(`src/sc_rpi/commands/base.py`), a mashumaro `DataClassJSONMixin` dataclass that uses a
**Discriminator on the `command_name` field** to deserialize incoming JSON directly into
the right concrete subclass — there is no manual if/elif dispatch on command name.

Key rules when adding or touching a command (see the docstring in `commands/base.py` for
the full list):
- The subclass must set `command_name` to the snake_case command name (this is the
  discriminator value), and must be imported somewhere so mashumaro registers it.
- Build instances via `Command.from_dict_wrapper(data, config, hw_controller)`, never
  `from_dict`/`to_dict` directly — those would miss/leak the private `_config` and
  `_hw_controller` attributes.
- `run()` returns a `CommandResult` — a dict mapping **MQTT topic name -> payload**
  (either a `DataClassJSONMixin` or a raw string). The caller (`Worker`) publishes one
  message per topic in the dict; this is how a single command can update both the SC RPi
  result topic and a Home Assistant state topic in one go.
- Rendering the physical strip (`hw_controller.render()`) must be the last call in `run()`
  so nothing is pushed to the hardware before validation/logic has had a chance to raise.
- Keep `Command` subclasses stateless beyond their dataclass fields. Do not cache or
  mutate values on `self` inside `run()`/`validate()` — `_config` and `_hw_controller`
  are shared across threads.
- Commands never touch MQTT directly — that's the `Worker`'s job. All hardware state
  (sections: start/end LED range, color, on/off) is owned by `SectionsController`
  (`controllers/sections_controller.py`); `HardwareController` wraps it plus the actual
  strip-rendering calls.

### Request flow

1. `main.py` loads config, wires up a Paho MQTT `Client`, and starts a `Worker` thread.
2. `paho/callbacks.py` handles `on_connect`/`on_message` and pushes incoming MQTT messages
   onto the `Worker`'s internal queue (`worker.put_message`).
3. `Worker.run()` (single dedicated thread, `src/sc_rpi/worker.py`) pulls messages off the
   queue, decides whether the topic matches an HA command topic or the SC RPi command
   topic (`utils/topic_utils.py`), parses the JSON into a `Command` (via HA mapping or
   directly), calls `validate()` then `run()`, and publishes each topic/payload pair from
   the result. Exceptions (including `ApiError`) are caught and translated into an error
   result published to the SC RPi result topic via `utils/mappings.map_exception`.

### Config and models

`Config` and friends (`src/sc_rpi/config/`) are mashumaro dataclasses loaded from YAML
(`config.yaml` for normal use, `config_test.yaml` for tests) via
`utils/config/main.load_configurations`. Home Assistant wire-format types
(`HACommand`, `HAState`, `HAMQTTDiscoveryMessage`) live under `models/homeassistant/` and
are kept separate from SC RPi's own command/result models (`commands/results.py`,
`models/section_internal_representation.py`).

### Logging

The project is mid-migration from the standard `logging` module to `structlog` (see the
TODOs in `main.py`/`worker.py`) — new code in `main.py` and anything touching logging
should prefer `structlog.get_logger(__name__)`, but most existing modules still use
`logging.getLogger(__name__)`.

## Documentation map

- `doc/commands.md` — wire format for every MQTT command and its result/error shape.
- `doc/homeassistant.md` — Home Assistant/Mosquitto/Grafana integration and setup.
- `doc/linux.md` — Raspberry Pi OS setup, Alloy/Loki, systemd service, networking.
- `doc/development.md` — local dev environment, Ruff, VS Code config.
- `doc/circuit.md` — physical wiring for the LED strip.