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
