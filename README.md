# Strip Controller Raspberry

Receives [commands](/doc/commands.md) through WebSocket, process them and convert it to PWM signals for any W2812B LED strip using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library.

## Requirements

- Python: 3.8.18 (see [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources).
- [Poetry](doc/poetry.md).

## Installation

Before installing the server on the Raspberry Pi, take a look at [Building the circuit](/doc/circuit.md) to know how to build the circuit with W2812B LED strips.

Currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) or in other words it run as a daemon. This also allow the server to be automatically started after system boot.

So required steps to install and run sc-rpi are the following :

1. [Install required linux dependencies](/doc/required_linux_dependencies.md)
2. [Create the virtual environment](/doc/virtual_environments.md#creating-virtual-environments).
3. [Activate the virtual environment](/doc/virtual_environments.md#activating-the-environment).
4. [Install required Python dependencies with poetry](/doc/poetry.md#installing-dependencies).
5. [Configure network](/doc/network_configuration.md).
6. [Configure sc-rpi](/doc/configurations.md).
7. [Configure service](/doc/systemd_configuration.md).

## Development

1. Create the [virtual environment](/doc/virtual_environments.md)
2. Activate the environment
3. [Install development dependencies with poetry](/doc/poetry.md)
4. Run the server:
    ```bash
    python -m run_server
    ```

Refer to [doc/development](doc/development.md) for development tips and advices.

## Unit testing

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Invoke unittest: `python -m unittest discover` (from the root folder)

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Userspace Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
