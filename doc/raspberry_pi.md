# Raspberry Pi OS

## Common issues

In case SSH is not working, check if `ssh.service` is correctly enabled :

```bash
systemctl status ssh.service
```

If necessary enable it with `systemctl` :

```bash
systemctl enable ssh.service
```

> It may be necessary to run `systemctl` with `sudo`

## Useful commands

Transferring code with `rsync`

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

Get system architecture:

```bash
uname -m
```

To get the installed Linux distribution:

```bash
cat /etc/os-release
```

To backup and compress a disk :

```bash
sudo dd if=/dev/diskX bs=4M status=progress | gzip > image.img.gz
```
