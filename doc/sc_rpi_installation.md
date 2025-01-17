# SC Rpi installation

SC Rpi installation can be summarized in the following steps:

1. [Copy source code](#transferring-code-with-rsync).
2. [Create virtual environment](/doc/virtual_environments.md).
3. [Install dependencies with poetry](/doc/poetry.md).
4. [Set configurations](#configurations).
5. [Configure linux service](/doc/systemd_configuration.md).

## Transferring code with `rsync`

A good way to copy the code while developing changes is using `rsync` like this:

```bash
rsync --recursive \
  --progress \
  --archive \
  --exclude-from=.gitignore \
  --exclude-from=.pylintrc \
  --exclude=doc \
  --exclude=.git \
  --exclude=.gitignore \
   . user@ipaddress:~/dest/ 
```

For more information about `rsync` take a look at [this](https://gist.github.com/brunopk/37c9703b9bc82061d32303d99d29d9fb) Gist.

## Configurations

Configurations are set on config.ini file on the root folder. Here is the list of available properties :

- Section: `DEFAULT`
  - `env`: environment `dev` or `rpi`
  - `port`: server port
  - `host`: server address to listen for connections
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