# Poetry

Among other features, Poetry provides a mechanism to have different dependencies for different environments. For instance testing libraries are only available for development environment.

It may be convenient to install it **globally**:

```bash
pip install poetry
```

## Installing dependencies

To install dependencies in the Raspberry Pi :

```bash
 poetry install --only main --with rpi_ws281x
```

## Installing development dependencies

The dependencies required for running on Raspberry Pi are almost the same as those required for development, but there are some exceptions, for example :

- [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) which is the library used to control the strip, only works on the Raspberry which means its necessary to mock its method sin order to be run on any other system like macOS. So for this reason this project its provided with a [fake implementation of](../lib/rpi-ws281x/) that library.
- Similar to rpi_ws281x, any other system dependant libraries should be replaced for a fake implementation.
- Dependencies for unit testing.

So to install development dependencies :

```bash
poetry install 
```

Notice `--only main` and `--with rpi_ws281x` arguments are not used here. These arguments are for [Poetry groups](https://python-poetry.org/docs/managing-dependencies#dependency-groups).

## Links

- [Poetry](https://python-poetry.org/)
