# Poetry

Among other features, Poetry provides a mechanism to have different dependencies for different environments. For instance testing libraries are only available for development environment.

It may be convenient to install it **globally**:

```bash
pip install poetry
```

## Installing dependencies

To install dependencies in the Raspberry Pi :

1. Comment out all dependencies which are listed in "fakes" group.
2. Uncomment all dependencies which are listed in "rpi-deps" group.
3. Install dependencies :

```bash
poetry install
```

## Installing development dependencies

The dependencies required for running on Raspberry Pi are almost the same as those required for development, but there are some exceptions, for example :

- [rpi_ws281x](http://github.com/richardghirst/rpi_ws281x) which is the library used to control the strip, only works on the Raspberry which means its necessary to mock its method sin order to be run on any other system like macOS. So for this reason this project its provided with a [fake implementation of](../lib/rpi-ws281x/) that library.
- Similar to rpi_ws281x, any other system dependant libraries should be replaced for a fake implementation.
- Dependencies for unit testing.

So to install development dependencies :

1. Comment out all dependencies which are listed in "rpi-deps" group.
2. Uncomment all dependencies which are listed in "dev" group.
3. Install dependencies with the **same** command mentioned in [Installing development dependencies](/doc/poetry.md#installing-development-dependencies)

## Links

- [Poetry](https://python-poetry.org/)
- [Poetry groups](https://python-poetry.org/docs/managing-dependencies#dependency-groups)
