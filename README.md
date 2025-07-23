# SC RPi

**Provides a simple MQTT API to control WS2812B LED strips connected to a Raspberry Pi, which can also be integrated with Home Assistant.**

- For more information about how to build the circuit, see `doc/circuit.md`
- For more information about MQTT and how it's used in SC RPi, see `doc/mqtt.md`
- For API documentation, see `/doc/commands.md`

## Requirements

- Raspberry Pi 3 or newer versions with Raspberry Pi OS
- W2812B LED strip (see `/doc/circuit.md`)
- Python: 3.9.x
- Poetry
- An MQTT broker (see `/doc/mqtt.md`)

> **In order to avoid networking issues, it's preferable to use the Raspbian GNU/Linux 11 (bullseye) version. See `doc/network.md` to properly configure WiFi networks.**

## Installation

1. [Ensure the Raspberry Pi is properly connected to a wired (LAN) or wireless (WLAN) network](/doc/network.md)
2. [Install required Linux dependencies](/doc/required_linux_dependencies.md)
3. [Install SC RPI (Python application)](/doc/sc_rpi_installation.md)
4. [Configure Mosquitto broker](/doc/mqtt.md#mosquitto-broker-configuration)
5. [Configure SC RPi](/doc/configurations.md)
6. [Configure SC RPi as a Linux service](/doc/systemd_configuration.md)

    </br>

Optionally, SC RPi can be installed as a [service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) to start automatically after boot; see `/doc/systemd_configuration.md` for more information. For more information about Linux services and the Mosquitto broker, refer to `/doc/systemd_configuration.md` and `/doc/mqtt.md`, respectively.


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

- [Official Python distribution of the rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Official Poetry website](https://python-poetry.org/)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Building the circuit for SC RPI](doc/circuit.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
- [Linux network configuration](/doc/network_configuration.md)
- [Official MQTT protocol site](https://mqtt.org/)
- [Home Assistant MQTT integration](https://www.home-assistant.io/integrations/mqtt/)
