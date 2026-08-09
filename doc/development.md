# Development

## Development dependencies

To install development dependencies run `uv` with the `--only-group` argument :

```bash
uv sync --only-group dev 
```

The [rpi-ws281x](http://github.com/richardghirst/rpi_ws281x) which is the library used to control the strip, only works on the Raspberry which means its necessary to mock its method sin order to be run on any other system like macOS. So for this reason this project it's provided with a [mocked implementation](../lib/rpi-ws281x/) of this library, this is an example of some mocked libraries used in SC RPi. **Mocked libraries are located in the [`/lib`](/lib) folder.**

## Testing

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Invoke unittest: `python -m unittest discover`.

> **Run tests from the root folder of the project.**

## Ruff

**To check linting rules in the current folder**

```bash
ruff check .
```

**To check and fix rules in a file**

```bash
ruff check file.py --fix
```

## Loki

Though is not recommended, as it is not really necessary, Loki can be installed locally with Docker following instructions in the [Loki tutorial](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/) of the official documentation.

To install Loki with `apt-get` refer to the [Loki](/doc/linux.md#loki) section in [`/doc/linux.md`](/doc/linux.md).

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


