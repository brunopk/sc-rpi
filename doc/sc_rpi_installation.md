# SC RPI installation

SC RPI installation can be summarized in the following steps:

1. Copy source code (refer to the [Transferring code with `rsync`](#transferring-code-with-rsync) section below)
2. Create virtual environment (refer to `/doc/virtual_environments.md` for more information)
3. Install Python dependencies (refer to the [Installing dependencies with Poetry](#installing-applications-and-dependencies-with-poetry) section below)

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

## Installing dependencies with Poetry

Before installing dependencies :

1. Comment out all dependencies below `[tool.poetry.group.dev.dependencies]`
2. Uncomment all dependencies below `[tool.poetry.group.rpi-only-deps.dependencies]`

Then invoke `poetry`:

```bash
poetry install
```

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)