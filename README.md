# SC RPi

**A lightweight MQTT-based API for controlling WS2812B LED strips connected to a Raspberry Pi from the Home Assistant web or mobile application.**

It also provides a simple MQTT-based API to sends [commands](doc/commands.md) directly, for example using an MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

>**The Raspberry Pi 3 uses the Broadcom BCM2837 SoC, which includes a hardware PWM controller and can be controlled from Python using the [`rpi_ws281x`](https://github.com/jgarff/rpi_ws281x) library.**

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS
- W2812B LED strip (see [`/doc/circuit.md`](/doc/circuit.md))
- Python
- Poetry
- An MQTT broker (see [`/doc/mqtt.md`](/doc/mqtt.md))

  </br>

## Installation

1. [Ensure the Raspberry Pi is properly connected to a wired (LAN) or wireless (WLAN) network](/doc/network.md)
2. [Install required Linux dependencies](/doc/required_linux_dependencies.md)
3. Install Docker to run the following containers (optional):
   - [Glances](https://glances.readthedocs.io/en/latest/docker.html#docker)
   - Grafana Loki
4. Install Home Assistant add-ons:
   - [Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto)
   - [Grafana](https://github.com/hassio-addons/addon-grafana) (optional)
5. [Install SC RPI (Python application)](/doc/sc_rpi_installation.md)
6. [Configure SC RPi](/doc/configurations.md)
7. [Configure SC RPi as a Linux service](/doc/systemd_configuration.md) (optional)
8. Configure Glances in Home Assistant as a new integration (optional)
9. Configure Grafana Loki datasource using the Grafana Home Assistant add-on (optional).
10. [Configure Mosquitto broker](/doc/mqtt.md#mosquitto-broker-configuration)

    </br>

## Development

1. [Create the virtual environment](/doc/virtual_environments.md)
2. [Activate the environment](/doc/virtual_environments.md#activating-the-environment)
3. [Install development dependencies with poetry](/doc/development.md#installing-development-dependencies)
4. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

For more information refer to `doc/development`.

## Documentation

SC RPi is provided with more documentation in the `doc` folders :

- [`doc/systemd_configuration.md`](doc/systemd_configuration.md): systemd configuration (Linux services)
- [`doc/mqtt.md`](doc/mqtt.md): information of MQTT, Mosquitto broker, etc.
- [`doc/network_configuration.md`](doc/network_configuration.md) : network configuration in Rapsberry OS
- [`doc/circuit.md`](doc/circuit.md): how to build the circuit for SC RPi
- [`doc/commands.md`](doc/commands.md): SC RPi commands (through MQTT)
- [`doc/development.md`](doc/development.md): useful documentation for SC RPi development

  </br>

## Links

- [Building the circuit for SC RPI](doc/circuit.md)
- [Glances with Docker](https://glances.readthedocs.io/en/latest/docker.html#docker)
- [Home Assistant MQTT integration](https://www.home-assistant.io/integrations/mqtt/)
- [Home Assistant Grafana add-on](https://github.com/hassio-addons/addon-grafana)
- [Home Assistant Mosquitto broker add-on](https://github.com/home-assistant/addons/tree/master/mosquitto)
- [Linux network configuration](/doc/network_configuration.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [Official MQTT protocol site](https://mqtt.org/)
- [Official Python distribution of the rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Official Poetry website](https://python-poetry.org/)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
