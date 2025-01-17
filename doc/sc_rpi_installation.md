# SC Rpi installation

SC Rpi installation can be summarized in the following steps:

1. [Copy source code](#transferring-code-with-rsync).
2. [Create virtual environment](/doc/virtual_environments.md).
3. [Install dependencies with poetry](/doc/poetry.md).

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

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)