# Configurations

SC RPi reads YAML files from the `config/` directory, resolved from the working directory.

- `config/default.yaml`: the boot configuration, read at startup. It is git-ignored because it contains MQTT credentials.
- `config/default.example.yaml`: committed example. On a fresh clone copy it:

  ```bash
  cp config/default.example.yaml config/default.yaml
  chmod 600 config/default.yaml
  ```

- `config/<name>.yaml`: saved configurations, also git-ignored.
- [`config_test.yaml`](../config_test.yaml) (repository root): used by unit tests.

## Properties

- `env`: `dev` or `rpi`
- `description`: optional free text (defaults to an empty string)
- `default_gateway`: default gateway used to test the connection
- `default_network_interface`: network interface used to test the connection
- `connection_timeout`: connection test timeout in seconds (float)
- `status_led`: GPIO pin of the status LED (BCM mode)
- `log_level`: `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`
- `mqtt`:
  - `broker`:
    - `host`: MQTT broker address
    - `port`: MQTT broker port
    - `username`: MQTT username
    - `password`: MQTT password
- `strip`:
  - `strip_length`: number of LEDs
  - `pin`: GPIO pin connected to the strip (18 uses PWM)
  - `freq_hz`: signal frequency in hertz (usually 800000)
  - `dma`: DMA channel (try 10)
  - `brightness`: 0 (darkest) to 255 (brightest)
  - `default_section_brightness`: brightness reported to Home Assistant for sections
  - `invert`: `True` when using an NPN transistor level shifter
  - `channel`: `1` for GPIOs 13, 19, 41, 45 or 53, otherwise `0`
  - `sections`: list of sections, each with:
    - `id`: unique identifier
    - `name`: human readable name
    - `start`: first LED of the section
    - `end`: last LED of the section (inclusive)
    - `is_on`: whether the section is on
    - `color`:
      - `r`: red (0-255)
      - `g`: green (0-255)
      - `b`: blue (0-255)
