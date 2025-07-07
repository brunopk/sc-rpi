# Strip Controller Raspberry

Provides an MQTT API to control WS2812B LED strips connected to a Raspberry Pi via GPIO, using the [rpi-ws281x](https://github.com/rpi-ws281x/rpi-ws281x-python). **It also integrates with Home Assistant (HA) by listening to specific MQTT topics defined by HA to discover entities and update their states (see [MQTT integration with HA](/doc/mqtt.md#mqtt-integration-with-ha) and [Mosquitto broker](/doc/mqtt.md#mosquitto-broker) in `/doc/mqtt.md`)**.

For more information about building the circuit and the API documentation, see `/doc/circuit.md` and `/doc/commands.md`, respectively.

## Requirements

- Raspberry Pi 3 or newer versions with [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- W2812B LED strip (see `/doc/circuit.md`)
- Python: 3.8.18
- Poetry
- An MQTT broker (see [Mosquitto broker](/doc//mqtt.md#mosquitto-broker) `/doc/mqtt.md`)

**It's strongly recommended to install [MQTT Explorer](https://mqtt-explorer.com/) for MQTT development and troubleshooting. It can be installed on macOS using Homebrew. This application is extremely helpful when working with MQTT topics and diagnosing issues.**

## Installation

SC RPI can be be manually installed as a [Linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). The steps to install it can be summarized in the following steps :

1. [Install required Linux dependencies](/doc/required_linux_dependencies.md)
2. [Install SC RPI (Python application)](/doc/sc_rpi_installation.md)
3. [Configure Mosquitto broker](/doc/mqtt.md#mosquitto-broker-configuration)
4. [Configure SC RPI](/doc/configurations.md)
5. [Configure SC RPI as a Linux service](/doc/systemd_configuration.md)

    </br>

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
