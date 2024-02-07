# Strip Controller Raspberry

Receives commands from the [sc-master](https://github.com/brunopk/sc-master) using the [SCP protocol](/doc/SCP_Protocol.md), process them and convert it to signals for any W2812B LED strip, using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library. Runs on the Raspberry Pi 3 with Python 3.7 or 3.8 .

## Building the circuit

1. With level shifter conversor:

![GitHub Logo](/doc/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

More information: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

2. Without level shifter conversor:
![GitHub Logo](/doc/raspberry-pi-updated-schematic.png)
More information: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html

## Installation

Currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) or in other words it run as a daemon. This also allow the server to be automatically started after system boot.

So required steps to install and run sc-rpi are the following :

1. [Configure network](/doc/network_configuration.md).
2. In order for Python systemd-python library to work, first install libsystemd-dev :

    ```bash
    sudo apt install libsystemd-dev
    ```

    as described here [here](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).

3. [Create the virtual environment](/doc/virtual_environments.md)
4. [Configure the service](/doc/service_configuration.md).

Server configuration can be found in config.ini

## Development

1. Create the [virtual environment](/doc/virtual_environments.md).
2. Activate the environment.
3. Run the server:

    ```bash
    python -m run_server
    ```

By default, the server logs on the `sc-rpi.log` file (on the root folder) and also in console. To disable console logging, remove the `console` property on the configuration file `config.ini`.

### Running automatic tests

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
