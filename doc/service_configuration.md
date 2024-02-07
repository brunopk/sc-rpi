# Service configuration

As mentioned on the [README.md](/README.md), currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) following these steps:

1. Create the configuration in /etc/systemd/system/ with something like this:

    ```conf
    [Unit]
    Description=sc-rpi server
    After=network.target

    [Service]
    Type=simple
    ExecStart=<path to the virtual env>/bin/python <path to sc-rpi>/run_server.py
    WorkingDirectory=<path to sc-rpi>
    User=root

    [Install]
    WantedBy=multi-user.target
    ```

2. Enable the service :

   ```bash
   systemctl enable sc-rpi.service
   ```


To check the server is correctly started :

```bash
systemctl status sc-rpi.service
```

Also logs can be obtained with [journal command](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs). So the output of this command :

```bash
journalctl -u sc-rpi.service
```

should be something like this :

```txt
Feb 06 23:42:03 raspberrypi systemd[1]: Started sc-rpi server.
Feb 06 23:42:04 raspberrypi <path to sc-rpi>/run_server.py[559]: sc-rpi server started.
Feb 06 23:42:04 raspberrypi systemd[1]: sc-rpi.service: Succeeded.
```
