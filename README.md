# Strip Controller Raspberry

Provides an [MQTT](https://mqtt.org/) API to control WS2812B LED strips connected to a Raspberry Pi via GPIO ports (see `/doc/circuit.md` for more information). The API consists of [commands](doc/commands.md) sent over MQTT topics. It also integrates with Home Assistant (HA) by listening to specific MQTT topics defined by HA to discover entities and update their states.

## Requirements

- Raspberry Pi 3 or newer versions with [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- W2812B LED strip (see `/doc/circuit.md`)
- Python: 3.8.18
- [Poetry](https://python-poetry.org/)
- An MQTT broker (see `/doc/mosquitto.md`)

## Installation

SC RPI can be be manually installed as a [Linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). The steps to install it can be summarized in the following steps :

1. [Install required Linux dependencies](/doc/required_linux_dependencies.md)
2. [Install SC RPI (Python application)](/doc/sc_rpi_installation.md)
3. [Configure Mosquitto add-on in HA](/doc/mosquitto.md)
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

- [Building the circuit](doc/circuit.md)
- [Linux network configuration](/doc/network_configuration.md)
- [Official MQTT site](https://mqtt.org/)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Official Poetry website](https://python-poetry.org/)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [User-space Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
