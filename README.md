# SC RPi

**Control WS2812B LED strips connected to a Raspberry Pi with the Home Assistant web interface or the mobile application via [MQTT](https://mqtt.org/).** 

It also provides a simple **MQTT-based API** to send [commands](doc/commands.md) directly, for example, using a MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS 64 bit version.
- W2812B LED strip (refer to [`/doc/circuit.md`](/doc/circuit.md) for more information).
- uv (Python package manager).
- Home Assistant (real or virtual server).


## Installation

### Home Assistant

1. [Install and configure the Mosquitto app](/doc/homeassistant.md#mosquitto-broker)
2. [Install and configure Grafana app](https://github.com/hassio-addons/addon-grafana)
3. [Install and configure the MQTT integration](https://www.home-assistant.io/integrations/mqtt/)

Optionally :
- Install [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) to debug MQTT messages.
- Install [Glances](/doc/homeassistant.md#glances) app and the corresponding integration to monitor resources in the Raspberry Pi.

Additional information :
- For more information about MQTT in Home Assistant refer to [`/doc/homeassistant.md`](/doc/homeassistant.md).

</br>

### Raspberry Pi

1. [Upload the code to the Raspberry Pi](/doc/linux.md#useful-commands)
2. [Install Loki](/doc/linux.md#loki)
3. Install Python dependencies with `uv` :

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
- Install [Glances](/doc/linux.md#glances) to remotely monitor hardware resources.
- Install SC RPi as a Linux service (refer to the [Systemd configuration](/doc/linux.md#systemd-configuration) section in [`/doc/linux.md`](/doc/linux.md)).

Additional information :
- For more information about wired and wireless network configuration in Linux refer to the [Network configuration](/doc/linux.md#network-configuration) section in [`/doc/linux.md`](/doc/linux.md).
- For more information about the uv package manager, refer to the [`uv`](/doc/development.md#uv) section in [`doc/development`](doc/development.md).

</br>

## Development

1. [Install and configure the Mosquitto app for Home Assistant](/doc/homeassistant.md#mosquitto-broker).
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

Optionally:

- Install the whole Grafana stack locally with Docker (refer to the [Loki](/doc/development.md#loki) section in [`/doc/development.md`](/doc/development.md)).
- Install [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) app for Home Assistant to debug MQTT messages.

</br>

## Documentation

- [`doc/circuit.md`](/doc/circuit.md): how to build the circuit for SC RPi
- [`doc/commands.md`](/doc/commands.md): describes SC RPi commands
- [`doc/development.md`](/doc/development.md): useful documentation for SC RPi development
- [`doc/homeassistant.md`](/doc/homeassistant.md): recommended add-ons, configurations and more for Home Assistant
- [`doc/linux.md`](/doc/linux.md): Linux documentation related to SC RPi

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Building the circuit for SC RPI](doc/circuit.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [MQTT protocol official site](https://mqtt.org/)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [uv package manager (official site)](https://docs.astral.sh/uv/#highlights)
- [Using Loki, Alloy and Grafana locally](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)

