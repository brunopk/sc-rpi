# SC RPi

**Control WS2812B LED strips connected to a Raspberry Pi with the Home Assistant web interface or the mobile application via [MQTT](https://mqtt.org/).** 

It also provides a simple **MQTT-based API** to send [commands](doc/commands.md) directly, for example, using a MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS 64 bit version (refer to [`/doc/raspberry_pi.md`](/doc/raspberry_pi.md) for more information).
- W2812B LED strip (refer to [`/doc/circuit.md`](/doc/circuit.md) for more information).
- uv (Python package manager).
- A running instance of Home Assistant (real or virtual server).
- An MQTT broker (refer to [Installation](#installation) section below for more information).

## Installation

### Home Assistant

1. [Install and configure the Mosquitto app](/doc/homeassistant.md#mosquitto-broker)
2. [Install and configure Grafana app](https://github.com/hassio-addons/addon-grafana)
3. [Install and configure the MQTT integration](https://www.home-assistant.io/integrations/mqtt/)

Optionally :
- Install MQTT Explorer to debug MQTT messages, refer to the [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) section in [`/doc/homeassistant.md`](/doc/homeassistant.md#mqtt-explorer) for more information.
- Install Glances app and the corresponding Glances integration to monitor resources in the Raspberry Pi, refer to the [glances](https://github.com/brunopk/sc-rpi/blob/feature/refact/doc/homeassistant.md#glances) section in [`/doc/homeassistant.md`](/doc/homeassistant.md) for more information.

Additional information :
- For more information about MQTT in Home Assistant refer to [`/doc/homeassistant.md`](/doc/homeassistant.md).

</br>

### Raspberry Pi

1. [Upload the code to the Raspberry Pi](/doc/raspberry_pi.md#useful-commands)
2. [Install loki](/doc/linux_dependencies.md#loki)
3. Install Python dependencies with `uv`:

    ```bash
    uv sync --group rpi
    ```
4. Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```
5. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

Optionally : 
- Install Glances to remotely monitor hardware resources, refer to [glances](/doc/linux_dependencies.md#glances) section in [`/doc/linux_dependencies.md`](/doc/linux_dependencies.md) for more information.
- Install SC RPi as a Linux service, refer to [`doc/systemd_configuration.md`](doc/systemd_configuration.md).

Additional information :
- For more information about wired and wireless network configuration in Linux refer to [`/doc/network_configuration.md`](/doc/network_configuration.md).
- For more information about the uv package manager, refer to the [`uv`](/doc/development.md#uv) section in [`doc/development`](doc/development.md).

</br>

## Development

1. [Install and configure the Mosquitto app for Home Assistant](/doc/homeassistant.md#mosquitto-broker) (SC RPi will connect to Home Assistant to use the Mosquitto MQTT broker).
2. Install development dependencies with `uv`:

   ```bash
   uv sync --group dev
   ```
3. Activate the virtual environment :

   ```bash
   source .venv/bin/activate
   ```
4. Run the application :

   ```bash
   python -m sc_rpi.main
   ```

Otionally:

- Install the whole Grafana stack locally by following instructions in the [Loki Tutorial](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/) section of the official documentation.
- Install [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) app for Home Assistant to debug MQTT messages.

</br>

## Documentation

- [`doc/circuit.md`](doc/circuit.md): how to build the circuit for SC RPi
- [`doc/commands.md`](doc/commands.md): describes SC RPi commands
- [`doc/development.md`](doc/development.md): useful documentation for SC RPi development
- [`doc/linux_dependencies.md`](/doc/linux_dependencies.md)
- [`doc/network_configuration.md`](doc/network_configuration.md) : network configuration in Raspberry Pi OS
- [`doc/homeassistant.md`](/doc/homeassistant.md): recommended add-ons, configurations and more for Home Assistant
- [`/doc/raspberry_pi.md`](/doc/raspberry_pi.md): common issues and useful commands
- [`doc/systemd_configuration.md`](doc/systemd_configuration.md): systemd configuration (Linux services)

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Building the circuit for SC RPI](doc/circuit.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [MQTT protocol (official site)](https://mqtt.org/)
- [rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python) (TODO: move this for development.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [uv package manager (official site)](https://docs.astral.sh/uv/#highlights)
- [Using Loki, Alloy and Grafana locally](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)

