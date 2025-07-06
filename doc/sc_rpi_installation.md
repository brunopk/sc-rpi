# SC RPI installation

SC RPI installation can be summarized in the following steps:

1. Copy source code (see [Transferring code with `rsync`](#transferring-code-with-rsync) below)
2. Create virtual environment (see `/doc/virtual_environments.md` for more information)
3. Install the application with Poetry (see [Installing applications and dependencies with Poetry](#installing-applications-and-dependencies-with-poetry) below)

</br>

Logs will be managed with journal and can be obtained with this :

```bash
journalctl -u sc-rpi.service
```

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

## Installing applications and dependencies with Poetry

To install dependencies in the Raspberry Pi :

1. Comment out all dependencies which are listed in `dev` group.
2. Uncomment all dependencies which are listed in `rpi-only-deps` group.
3. Install dependencies :

```bash
poetry install
```

> This will install the dependencies in the virtual environment directories, along with the application. This means the application will be installed as a Python module, just like any other dependency.

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)