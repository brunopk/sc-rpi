# SC RPi

**Control WS2812B LED strips connected to a Raspberry Pi from the Home Assistant web or from its mobile application through [MQTT](https://mqtt.org/).** 

It also provides a simple MQTT-based API to sends [commands](doc/commands.md) directly, for example using a MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

</br>

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS (refer to [`/doc/raspberry_pi.md`](/doc/raspberry_pi.md) for more information).
- W2812B LED strip (refer to [`/doc/circuit.md`](/doc/circuit.md) more information).
- uv (Python package manager).
- A running instance of Home Assistant (real or virtual server).
- An MQTT broker (refer to [`/doc/mqtt.md`](/doc/mqtt.md) for more information).

  </br>

<!-- Notes:
64 bit version of Raspberry Pi OS is required for [Grafana Loki](doc/linux_dependencies.md#loki). -->

Python interpreter can be installed with `uv` (refer to the [uv](doc/development.md#uv) section in [`doc/development.md`](/doc/development.md#uv) for more information). Refer to [`doc/linux_dependencies.md`](doc/linux_dependencies.md) for more information about other not mandatory but useful software to install on the Raspberry.



## Installation

1. [Install and configure the Mosquitto app for Home Assistant](/doc/homeassistant.md#mosquitto-broker)
2. [Install and configure the MQTT integration for Home Assistant](https://www.home-assistant.io/integrations/mqtt/)
3. [Install and configure SC RPi on the Raspberry Pi](/doc/sc_rpi_installation.md)

    </br>

Additional information:
</br>
- For more information about network configuration refer to [`/doc/network_configuration.md`](/doc/network_configuration.md).
- For more information about MQTT and Home Assistant refer to [`/doc/homeassistant.md`](/doc/homeassistant.md).
- To install SC RPi as a Linux service refer to [`doc/systemd_configuration.md`](doc/systemd_configuration.md).

  </br>


## Development

1. [Activate the environment](/doc/virtual_environments.md#activating-the-environment)
2. [Install development dependencies with `uv`](/doc/development.md#installing-development-dependencies)
3. [Install and configure MQTT Explorer add-on for Home Assistant (optional)](/doc/homeassistant.md#mqtt-explorer)
4. [Upload the code to the Raspberry Pi](/doc/sc_rpi_installation.md#transferring-code-with-rsync)
5. [Install Python dependencies with `uv`](/doc/sc_rpi_installation.md#transferring-code-with-rsync)
6. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

    </br>

With `uv`, the virtual environment will be created automatically, for more information about `uv`, refer to the [`uv`](/doc/development.md#uv) section in [`doc/development`](doc/development.md). For more information about virtual environments refer to [`/doc/virtual_environments.md`](/doc/virtual_environments.md).

## Documentation

- [`doc/circuit.md`](doc/circuit.md): how to build the circuit for SC RPi
- [`doc/commands.md`](doc/commands.md): describes SC RPi commands
- [`doc/development.md`](doc/development.md): useful documentation for SC RPi development
- [`doc/linux_dependencies.md`](/doc/linux_dependencies.md)
- [`doc/network_configuration.md`](doc/network_configuration.md) : network configuration in Raspberry Pi OS
- [`doc/homeassistant.md`](/doc/homeassistant.md): recommended add-ons, configurations and more for Home Assistant
- [`/doc/raspberry_pi.md`](/doc/raspberry_pi.md): common issues and useful commands
- [`doc/systemd_configuration.md`](doc/systemd_configuration.md): systemd configuration (Linux services)

  </br>

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Building the circuit for SC RPI](doc/circuit.md)
- [Grafana Loki](doc/linux_dependencies.md#loki)
- [Linux network configuration](/doc/network_configuration.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [Official MQTT protocol site](https://mqtt.org/)
- [Official Paho PyPI website](https://pypi.org/project/paho-mqtt/)
- [Official Python distribution of the rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [uv package manager](https://docs.astral.sh/uv/#highlights)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
  
  </br>
