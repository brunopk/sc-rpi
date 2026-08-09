# Building the circuit for SC RPI

>**The Raspberry Pi 3 uses the Broadcom BCM2837 SoC, which includes a hardware PWM controller and can be controlled from Python using the [`rpi_ws281x`](https://github.com/jgarff/rpi_ws281x) library.**

## With level shifter convertor

![GitHub Logo](/doc/img/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

## Without level shifter convertor

![GitHub Logo](/doc/img/raspberry-pi-updated-schematic.png)

To quickly test the strip with Python:

1. Download [`strandtest.py`](https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py) (provided with the [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) library)
2. Create a virtual environment (more information about virtual environments in [`doc/virtual_environments.md`](/doc/virtual_environments.md))
3. Run `strandtest.py` (with `sudo` in order to properly work with the required hardware) :

   ```bash
   sudo ./venv/bin/python strandtest.py
   ```

   Where `venv` is the directory for the virtual environment.

   </br>

## Links

- [Connect and Control WS2812 RGB LED Strips via Raspberry Pi](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/#google_vignette)
- [WS2812 / NeoPixel Addressable LEDs: Raspberry Pi Quickstart Guide](https://core-electronics.com.au/guides/ws2812-addressable-leds-raspberry-pi-quickstart-guide/)
