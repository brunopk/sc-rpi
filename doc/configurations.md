# Configurations

Configurations are set on config.ini file on the root folder. Here is the list of available properties :

- Section: `DEFAULT`
  - `env`: environment
  - `port`: server port
  - `host`: server address to listen for connections
  - `tcp_max_queue`: socket configuration for messages received through TCP protocol
  - `tcp_max_msg_size`: max size in bytes
  - `tcp_msg_encoding`: message encoding (usually UTF-8)
- Section `CONNECTION_CHECK`:
  - `default_gateway`: default gateway to test connection before listening for client connections
  - `status_led`: GPIO port (BCM mode)
  - `iface`: interface to use to test connection
  - `timeout`: timeout (float value)
- Section: `PIXEL_STRIP`:
  - `n`: number of led pixels in the strip.
  - `pin`: GPIO pin connected to the pixels (18 uses PWM!).
  - `freq_hz`: led signal frequency in hertz (usually 800khz)
  - `dma`: DMA channel to use for generating signal (try 10)
  - `brightness`: Set to 0 for darkest and 255 for brightest
  - `invert`: `True` to invert the signal (when using NPN transistor level shift)
  - `channel`: set to '1' for GPIOs 13, 19, 41, 45 or 53, otherwise 0
- Section [LOGGING]
  - `level`: DEBUG, INFO, WARNING, ERROR, CRITICAL (refer to the [Python Logging library](https://docs.python.org/3.1/library/logging.html) for more information).

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)