# Strip Controller Driver

Receives commands from the [sc-master](https://github.com/brunopk/sc-master), process them and convert it to signals for the W2812B strips using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library. It's part of the sc project and it runs on Raspberry Pi 3. 

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

## Building the circuit

1. With level shifter conversor:

![GitHub Logo](/doc/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

More information: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

2. Without level shifter conversor: 
![GitHub Logo](/doc/raspberry-pi-updated-schematic.png)
More information: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- https://github.com/rpi-ws281x/rpi-ws281x-python 
- http://github.com/richardghirst/rpi_ws281x

