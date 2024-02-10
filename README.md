# Strip Controller Raspberry

Receives commands from the [sc-master](https://github.com/brunopk/sc-master) using the [SCP protocol](/doc/SCP_Protocol.md), process them and convert it to signals for any W2812B LED strip, using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library.

## Requirements

- Python: 3.8.18 (follow steps [here](https://forums.raspberrypi.com/viewtopic.php?t=291158) to install it from sources).
- [Poetry](doc/poetry.md).

## Installation

### Installation on Raspberry Pi

Before installing the server on the Raspberry Pi, take a look at [Building the circuit](/doc/circuit.md) to know how to build the circuit with W2812B LED strips.

Currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) or in other words it run as a daemon. This also allow the server to be automatically started after system boot.

So required steps to install and run sc-rpi are the following :

1. [Configure network](/doc/network_configuration.md).
2. [Install required linux dependencies](/doc/required_linux_dependencies.md)
3. [Create the virtual environment](/doc/virtual_environments.md#creating-virtual-environments) and [activate it](/doc/virtual_environments.md#activating-the-environment).
4. [Install dependencies with poetry](/doc/poetry.md#installing-dependencies)
5. [Configure the service](/doc/service_configuration.md).

Server configuration can be found in config.ini

### Development environment

1. Create the [virtual environment](/doc/virtual_environments.md).
2. Activate the environment.
3. [Install development dependencies with poetry](/doc/poetry.md)
4. Run the server:

    ```bash
    python -m run_server
    ```

By default, the server logs on the `sc-rpi.log` file (on the root folder) and also in console. To disable console logging, remove the `console` property on the configuration file `config.ini`.

#### Unit testing

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Invoke unittest: `python -m unittest discover` (from the root folder)

## Future improvements

- Timout functionality in case of no receiving commands.
- Automatic stress testing to send multiple commands in a short period of time.
- Document errors.
- Differentiate errors (return bad request, conflict, etc)

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Userspace Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
