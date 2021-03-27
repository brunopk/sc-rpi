# Strip Controller Raspberry

Receives commands from the [sc-master](https://github.com/brunopk/sc-master) using the [SCP protocol](/doc/SCP_Protocol.md), process them and convert it to signals for any W2812B LED strip, using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library. Runs on the Raspberry Pi 3 with Python 3.7 or 3.8 . 

## Starting the server

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Go to `src` folder: `cd src`
3. Give execution permissions to the main script: `chmod +x main.py`
4. Start the main script: './main.py'

## Creating a virtual environment (venv)

```
python3 -m venv <path of the venv>
```

or

```
virtualenv -m <path to the python interpreter> <path of the venv>
```

## Running automatic tests

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Go to `src` folder: `cd src`
3. Invoke unittest: `python -m unittest discover`

## Building the circuit

1. With level shifter conversor:

![GitHub Logo](/doc/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

More information: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

2. Without level shifter conversor: 
![GitHub Logo](/doc/raspberry-pi-updated-schematic.png)
More information: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html

## Future improvements

- Timout functionality in case of no receiving commands.
- Automatic stress testing to send multiple commands in a short period of time.
- Document errors 
- Differentiate errors (return bad request, conflict, etc)


## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Official Python distribution of the ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python)
- [Userspace Raspberry Pi PWM library for WS281X LEDs](http://github.com/richardghirst/rpi_ws281x)

