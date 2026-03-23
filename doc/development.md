# Development

## `uv`

`uv` is a Python package manager developed in Rust with many binaries distributions that can be easily installed on different operative systems. Among other features, `uv` provides a mechanism to have different dependencies for different environments.

### Installing dependencies 

```bash
uv sync --only-group rpi
```

</br>

**`uv sync` create the virtual environment automatically**. For more information about virtual environments refer to [`/doc/virtual_environments.md`](/doc/virtual_environments.md). **Use this command on the Raspberry Pi, not for development on other systems.**

### Installing development dependencies

To install development dependencies run `uv` like this:

```bash
uv sync --only-group dev 
```

The [rpi-ws281x](http://github.com/richardghirst/rpi_ws281x) which is the library used to control the strip, only works on the Raspberry which means its necessary to mock its method sin order to be run on any other system like macOS. So for this reason this project it's provided with a [mocked implementation](../lib/rpi-ws281x/) of this library, this is an example of some mocked libraries used in SC RPi. **Mocked libraries are located in the [`/lib`](/lib) folder.**

# Ruff

**To check linting rules in the current folder**

```bash
ruff check .
```

**To check and fix rules in a file**

```bash
ruff check file.py --fix
```

## Testing

1. Create a virtual environment (venv) if it's not created yet
2. Activate the venv: `source <path of the venv>/bin/activate`
3. Invoke unittest: `python -m unittest discover` (from the root folder)

## Visual Code

### Running Python applications with Visual Code

In order to run the application as a Python module :

1. Create the `launch.json` configuration file into `.vscode/`:

    ```json
    {
     "version": "0.2.0",
      "configurations": [
        {
          "name": "Run",
          "type": "debugpy",
          "request": "launch",
          "module": "sc_rpi.main"
        }
      ]
    }
    ```

2. Create the `settings.json` configuration file into `.vscode/`:

    ```json
    {
      "python.analysis.extraPaths": ["src"]
    }
    ```

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Mashumaro](https://pypi.org/project/mashumaro/)
- [Paho PyPI website](https://pypi.org/project/paho-mqtt/)
- [Paho documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
- [Python virtual environments](virtual_environments.md)
- [uv package manager official site](https://docs.astral.sh)
