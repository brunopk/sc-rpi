# Strip Controller Raspberry

Receives [commands](/doc/commands.md) through WebSocket, process them and convert it to PWM signals for any W2812B LED strip using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library. The circuit to connect the strip to the Raspberry Pi is described [here](/doc/circuit.md).

## Requirements

- Raspberry Pi 3 or newer versions with [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/).
- W2812B LED strip.
- Python: 3.8.18.
- [Poetry](doc/poetry.md)

> In case of not being able to install Python with apt-get (`sudo apt-get install python3.8`), refer to [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources.

## Installation

Currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). This also allow the server to be automatically started after system boot. So required steps to install and run sc-rpi are the following :

1. [Install required linux dependencies](/doc/required_linux_dependencies.md).
2. [Install sc-rpi](/doc/sc_rpi_installation.md).
3. [Set configurations](/doc/configurations.md).
4. [Configure linux service](/doc/systemd_configuration.md).

Logs will be managed with journal and can be obtained with this :

```bash
journalctl -u sc-rpi.service
```

For more information refer to [/doc/systemd_configuration](/doc/systemd_configuration.md).

## Development

1. Create the [virtual environment](/doc/virtual_environments.md)
2. Activate the environment
3. [Install development dependencies with poetry](/doc/poetry.md)
4. Run the server:

    ```bash
    python -m main
    ```

Refer to [doc/development](doc/development.md) for development tips and advices.

## Unit testing

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Invoke unittest: `python -m unittest discover` (from the root folder)

## Links

- [Network configuration in Raspberry Pi OS](/doc/network_configuration.md).
- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Userspace Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)
