# Development

## Poetry

Among other features, Poetry provides a mechanism to have different dependencies for different environments. For instance testing libraries are only available for development environment.

It may be convenient to install it **globally**:

```bash
pip install poetry
```

> Ensure that after invoking any `poetry` command the following section is still present in `pyproject.toml` :
>
> ```toml
> [tool.poetry.group.rpi-only-deps.dependencies]
> #systemd-python = "235"
> #"RPi.GPIO" = "0.7.1"
> #rpi-ws281x = "5.0.0"
> ```

### Installing development dependencies

The dependencies required for running on Raspberry Pi are almost the same as those required for development, but there are some exceptions, for example :

- [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) which is the library used to control the strip, only works on the Raspberry which means its necessary to mock its method sin order to be run on any other system like macOS. So for this reason this project its provided with a [fake implementation of](../lib/rpi-ws281x/) that library.
- Similar to rpi_ws281x, any other system dependant libraries should be replaced for a fake implementation.
- Dependencies for unit testing.

So to install development dependencies :

1. Comment out all dependencies which are listed in `rpi-only-deps` group.
2. Uncomment all dependencies which are listed in `dev` group.
3. Install all dependencies including `dev` dependencies :

    ```bash
    poetry install --with=dev 
    ```

### Adding new dependencies

To add new development dependencies :

```bash
poetry add --group=dev <DEPENDENCY_NAME>
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

## Transferring code to the Raspberry Pi

To facilitate development and testing on a Raspberry Pi, files can be efficiently transferred using `rsync` command, refer to [this](/doc/sc_rpi_installation.md#transferring-code-with-rsync) for more information.

> Verify your terminal is located in the root folder of the project before using `rsync`.

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Mashumaro](https://pypi.org/project/mashumaro/)
- [Official Paho PyPI website](https://pypi.org/project/paho-mqtt/)
- [Official Poetry website](https://python-poetry.org/)
- [Official Poetry website - Groups](https://python-poetry.org/docs/managing-dependencies#dependency-groups)
- [Paho documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
- [Python virtual environments](virtual_environments.md)
