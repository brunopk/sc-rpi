# SC RPi installation

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

## Links

- [Python logging library](https://docs.python.org/3.1/library/logging.html)
