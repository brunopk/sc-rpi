# Strip Controller Driver

sc-driver runs on Raspberry Pi 3. It receives commands from the [sc-master](https://github.com/brunopk/sc-master) process them and convert it to signals for the W2812B strips using the [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) library.

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

