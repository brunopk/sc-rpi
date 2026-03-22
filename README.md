# SC RPi

**Control WS2812B LED strips connected to a Raspberry Pi with the Home Assistant web interface or the mobile application via [MQTT](https://mqtt.org/).** 

</br>

It also provides a simple **MQTT-based API** to send [commands](doc/commands.md) directly, for example, using a MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/).

</br>

## Requirements

- Raspberry Pi 3 with Raspberry Pi OS 64 bit version (refer to [`/doc/raspberry_pi.md`](/doc/raspberry_pi.md) for more information).
- W2812B LED strip (refer to [`/doc/circuit.md`](/doc/circuit.md) for more information).
- uv (Python package manager).
- A running instance of Home Assistant (real or virtual server).
- An MQTT broker (refer to [Installation](#installation) section for more information).

  </br>


## Installation

1. [Install and configure the Mosquitto app for Home Assistant](/doc/homeassistant.md#mosquitto-broker)
2. [Install and configure the MQTT integration for Home Assistant](https://www.home-assistant.io/integrations/mqtt/)
3. [Install loki](/doc/linux_dependencies.md#loki)
4. [Upload the code to the Raspberry Pi](/doc/raspberry_pi.md#useful-commands)
5. Install Python dependencies with `uv`:

    ```bash
    uv sync --group rpi
    ```
6. Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```
7. Run the application :

    ```bash
    python -m sc_rpi.main
    ```

    </br>

Additional information:</br>
- For more information about wired and wireless network configuration in Linux refer to [`/doc/network_configuration.md`](/doc/network_configuration.md).
- For more information about MQTT in Home Assistant refer to [`/doc/homeassistant.md`](/doc/homeassistant.md).
- For more information about the uv package manager refer to the [`uv`](/doc/development.md#uv) section in [`doc/development`](doc/development.md).

  </br>

Optionally : 

- Install Glances to monitor hardware resources (refer to [glances](/doc/linux_dependencies.md#glances) section in [`/doc/linux_dependencies.md`](/doc/linux_dependencies.md)).
- Install MQTT Explorer in Home Assistant to debug MQTT messages (refer to the [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) section in [`/doc/homeassistant.md`](/doc/homeassistant.md#mqtt-explorer)).
- Install SC RPi as a Linux service (refer to [`doc/systemd_configuration.md`](doc/systemd_configuration.md)).

  </br>


## Development

1. [Install and configure the Mosquitto app for Home Assistant](/doc/homeassistant.md#mosquitto-broker)
2. Install development dependencies with `uv`:

   ```bash
   uv sync --group dev
   ```
4. Activate the virtual environment :

   ```bash
   source .venv/bin/activate
   ```
6. Run the application :

   ```bash
   python -m sc_rpi.main
   ```

    </br>


Optionally :</br>
- Install [MQTT Explorer](/doc/homeassistant.md#mqtt-explorer) app in Home Assistant to debug MQTT messages.

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

  </br>

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Building the circuit for SC RPI](doc/circuit.md)
- [Linux network configuration](/doc/network_configuration.md)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [Official MQTT protocol site](https://mqtt.org/)
- [Official Python distribution of the rpi_ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Python virtual environments](doc/virtual_environments.md)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
- [SC RPI commands](doc/commands.md)
- [Systemd configuration for SC RPI](/doc/systemd_configuration.md)
- [uv package manager](https://docs.astral.sh/uv/#highlights)
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
  
  </br>
