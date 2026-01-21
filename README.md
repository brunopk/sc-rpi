# SC RPi

**A lightweight [MQTT](https://mqtt.org/) API for controlling WS2812B LED strips connected to a Raspberry Pi from the Home Assistant web or mobile application.**

It also provides a simple MQTT-based API to sends [commands](doc/commands.md) directly, for example using an MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

</br>

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS
- W2812B LED strip (see [`/doc/circuit.md`](/doc/circuit.md))
- Python
- Poetry
- An MQTT broker (see [`/doc/mqtt.md`](/doc/mqtt.md))

  </br>

## Installation

1. [Install Linux dependencies](/doc/linux_dependencies.md)
2. [Install and configure Home Assistant add-ons (optional)](/doc/homeassistant.md#optional-add-ons)
3. [Install and configure Mosquitto broker](/doc/homeassistant.md#mosquitto-broker-required)
4. [Install and configure SC RPi (Python)](/doc/sc_rpi_installation.md)
5. [Install and configure Home Assistant MQTT integration](/doc/homeassistant.md#sc-rpi-integration-with-home-assistant)

    </br>

**[Ensure the Raspberry Pi is properly connected to a wired (LAN) or wireless (WLAN) network](/doc/network_configuration.md)**

## Development

1. [Create the virtual environment](/doc/virtual_environments.md)
2. [Activate the environment](/doc/virtual_environments.md#activating-the-environment)
3. [Install development dependencies with poetry](/doc/development.md#installing-development-dependencies)
4. [Install and configure MQTT Explorer add-on for Home Assistant (optional)](/doc/homeassistant.md#mqtt-explorer)
5. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

For more information refer to `doc/development`.

## Documentation

- [`doc/circuit.md`](doc/circuit.md): how to build the circuit for SC RPi
- [`doc/commands.md`](doc/commands.md): describes SC RPi commands
- [`doc/development.md`](doc/development.md): useful documentation for SC RPi development
- [`doc/docker.md`](/doc/docker.md): additional Docker containers to run in the Raspberry Pi
- [`doc/linux_dependencies.md`](/doc/linux_dependencies.md)
- [`doc/network_configuration.md`](doc/network_configuration.md) : network configuration in Raspberry Pi OS
- [`doc/homeassistant.md`](/doc/homeassistant.md): recommended add-ons, configurations and more for Home Assistant
- [`doc/systemd_configuration.md`](doc/systemd_configuration.md): systemd configuration (Linux services)

  </br>

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Building the circuit for SC RPI](doc/circuit.md)
- [Linux network configuration](/doc/network_configuration.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [Official MQTT protocol site](https://mqtt.org/)
- [Official Paho PyPI website](https://pypi.org/project/paho-mqtt/)
- [Official Python distribution of the rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Official Poetry website](https://python-poetry.org/)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
  
  </br>
