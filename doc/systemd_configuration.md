# Systemd configuration

As mentioned on the [README.md](/README.md), currently sc-rpi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). To do this follow these steps:

1. Create the configuration in /etc/systemd/system/ with something like this:

    ```conf
    [Unit]
    Description=sc-rpi server

    [Service]
    Type=simple
    ExecStart=/home/pi/sc-rpi/.direnv/bin/python /home/pi/sc-rpi/scripts/network_checker.py
    WorkingDirectory=/home/pi/sc-rpi/scripts
    User=root
    Restart=on-failure
    RestartSec=2

    [Install]
    WantedBy=multi-user.target
    ```

2. Enable the service :

   ```bash
   systemctl enable sc-rpi.service
   ```

</br>
</br>

To check the server is correctly started :

```bash
systemctl status sc-rpi.service
```

Also logs can be obtained with the [journal command line interface](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs). For example, with this command :

```bash
journalctl -u sc-rpi.service
```

something like this can be obtained :

```txt
Feb 06 23:42:03 raspberrypi systemd[1]: Started sc-rpi server.
Feb 06 23:42:04 raspberrypi <path to sc-rpi>/run_server.py[559]: sc-rpi server ready to listen new connections.
Feb 06 23:42:04 raspberrypi systemd[1]: sc-rpi.service: Succeeded.
```
