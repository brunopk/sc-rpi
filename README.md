# Strip Controller Raspberry

Receives commands from the [sc-master](https://github.com/brunopk/sc-master) using a custom [protocol](/doc/protocol.md) over TCP, process them and convert it to signals for any W2812B LED strip, using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library.

## Requirements

- Python: 3.8.18 (see [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources).
- [Poetry](doc/poetry.md).

## Configuration

Configurations are set on config.ini file on the root folder. Refer to [/doc/configurations](/doc/configurations.md) for more information.

## Installation

Before installing the server on the Raspberry Pi, take a look at [Building the circuit](/doc/circuit.md) to know how to build the circuit with W2812B LED strips.

Currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) or in other words it run as a daemon. This also allow the server to be automatically started after system boot.

So required steps to install and run sc-rpi are the following :

1. [Configure network](/doc/network_configuration.md).
2. [Install required linux dependencies](/doc/required_linux_dependencies.md)
3. [Create the virtual environment](/doc/virtual_environments.md#creating-virtual-environments).
4. [Activate the virtual environment](/doc/virtual_environments.md#activating-the-environment).
5. [Install dependencies with poetry](/doc/poetry.md#installing-dependencies)
6. [Configure systemd service](/doc/systemd_configuration.md).

## Development

1. Create the [virtual environment](/doc/virtual_environments.md)
2. Activate the environment
3. [Install development dependencies with poetry](/doc/poetry.md)
4. Run the server:
    ```bash
    python -m run_server
    ```

To facilitate development and testing on a Raspberry Pi, files can be efficiently transferred using this command:

```bash
rsync --recursive \
  --progress \
  --archive \
  --exclude-from=.gitignore \
  --exclude=.git \
  --exclude=.gitignore \
   folder user@ipaddress:~/dest/ 
```

## Unit testing

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Invoke unittest: `python -m unittest discover` (from the root folder)

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Userspace Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
