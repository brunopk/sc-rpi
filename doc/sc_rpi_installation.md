# SC RPI installation

SC RPI installation can be summarized in the following steps:

1. [Copy source code](#transferring-code-with-rsync).
2. [Create virtual environment](/doc/virtual_environments.md).
3. [Install dependencies and the main package (`sc_rpi`) with `poetry`](#installing-dependencies-with-poetry)

## Transferring code with `rsync`

An efficient way to transfer code to the Raspberry Pi is using `rsync`:

```bash
rsync --recursive \
  --progress \
  --archive \
  --exclude-from=.gitignore \
  --exclude=doc \
  --exclude=.git \
  --exclude=.gitignore \
   . user@ipaddress:~/dest/ 
```

For more information about `rsync` take a look at [this](https://gist.github.com/brunopk/37c9703b9bc82061d32303d99d29d9fb) Gist.

## Installing dependencies with Poetry

To install dependencies in the Raspberry Pi :

1. Comment out all dependencies which are listed in `dev` group.
2. Uncomment all dependencies which are listed in `rpi-only-deps` group.
3. Install dependencies :

```bash
poetry install
```

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)