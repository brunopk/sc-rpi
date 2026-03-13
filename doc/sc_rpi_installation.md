# SC RPI installation

SC RPI installation can be summarized in the following steps:

1. Copy source code (refer to the [Transferring code with `rsync`](#transferring-code-with-rsync) section below)
2. Install Python dependencies (refer to the [Installing dependencies with `uv`](#installing-applications-and-dependencies-with-uv) section below)

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

## Installing dependencies with `uv`

Invoke `uv` like this :

```bash
uv sync --only-group rpi
```

</br>

> `uv sync` create the virtual environment automatically (for more information about virtual environments refer to [`/doc/virtual_environments.md`](/doc/virtual_environments.md)).

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)