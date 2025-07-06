# Strip Controller Raspberry

Provides a Websocket API to control W2812B LED strips connected with a Raspberry Pi through GPIO ports. The API consists of [commands](doc/commands.md) transmitted via JSON-formatted messages over a WebSocket connection. See `/doc/circuit.md` for more information about the connection of the strip.

## Requirements

- Raspberry Pi 3 or newer versions with [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- W2812B LED strip (see `/doc/circuit.md`)
- Python: 3.8.18
- [Poetry](https://python-poetry.org/)

> In case of not being able to install Python with apt-get (`sudo apt-get install python3.8`), refer to [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources.

## Installation

SC RPI can be be manually installed as a [Linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). The steps to install it can be summarized in the following steps :

1. [Install required Linux dependencies](/doc/required_linux_dependencies.md)</br>
2. [Install SC RPI (Python application)](/doc/sc_rpi_installation.md)</br>
3. [Configure SC RPI](/doc/configurations.md)</br>
4. [Configure SC RPI as a Linux service](/doc/systemd_configuration.md)</br>

For more information about Linux services refer to `/doc/systemd_configuration`.

## Development

1. [Create the virtual environment](/doc/virtual_environments.md)
2. [Activate the environment](/doc/virtual_environments.md#activating-the-environment)
3. [Install development dependencies with poetry](/doc/development.md#installing-development-dependencies)
4. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

For more information refer to `doc/development`.

## Links

- [Async HTTP client/server for asyncio and Python](https://docs.aiohttp.org/en/stable/)
- [Building the circuit](doc/circuit.md)
- [Linux network configuration](/doc/network_configuration.md).
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Official Poetry website](https://python-poetry.org/)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [SC RPI systemd configuration](/doc/systemd_configuration.md)
- [User-space Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
