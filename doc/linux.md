# Linux for Raspberry Pi

## Systemd configuration

As mentioned on the [README.md](/README.md), currently SC RPi is intended to be manually installed as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services). To do this follow these steps:

1. Create the service configuration in */etc/systemd/system/* with something like this:

    ```conf
    [Unit]
    Description=sc-rpi server
    
    [Service]
    Type=simple
    ExecStart=/home/pi/sc-rpi/.direnv/bin/python /home/pi/sc-rpi/main.py
    WorkingDirectory=/home/pi/sc-rpi
    User=root
    Restart=on-failure
    RestartSec=2
    
    [Install]
    WantedBy=multi-user.target
    ```

    > Note that the Python executable should point to the virtual environment previously created.
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

### Restarting the service

```bash
systemctl restart sc-rpi.service
```

If service configuration was changed, reload configuration before restarting :

```bash
systemctl daemon-reload
```

### Logging

Also logs can be obtained with the [journal command line interface](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs). For example, with this command :

```bash
journalctl -u sc-rpi.service
```

something like this can be obtained :

```txt
Feb 06 23:42:03 raspberrypi systemd[1]: Started sc-rpi server.
Feb 06 23:42:04 raspberrypi <path to sc-rpi>/main.py[559]: sc-rpi server ready to listen new connections.
Feb 06 23:42:04 raspberrypi systemd[1]: sc-rpi.service: Succeeded.
```

## Network configuration

There're many ways to configure network in Linux :

- [Using Network Manager](#using-network-manager)
- [Using WPA supplicant (through configuration files)](#using-wpa-supplicant)

</br>

> **The preferred way to configure the network in Raspbian OS is using Network Manager.**

To check to which device is the Raspberry connected:

```bash
ifconfig
```

or :

```bash
iw wlan0 link
```

or :

```bash
iwconfig wlan0
```

or :

```bash
wpa_cli -i wlan0 STATUS   
```

</br>

> It may be necessary to run these commands with `sudo`.

### Using Network Manager

To connect to a WiFi network :

```bash
sudo nmcli device wifi connect "YourSSID" --ask
```

To discover WiFi networks (with or without `sudo`):

```bash
nmcli device wifi list
```

#### Using Network Manager with Raspbian GNU/Linux 11 (Bullseye)

Install Network Manager (if not installed yet):

```bash
sudo apt install network-manager
```

Disable `dhcpcd` service (optional but recommended to avoid conflicts) :

```bash
sudo systemctl disable dhcpcd
```

stop it:

```bash
sudo systemctl stop dhcpcd
```

Finally, enable Network Manager service :

```bash
sudo systemctl enable NetworkManager
```

and start it:

```bash
sudo systemctl start NetworkManager
```

#### Common errors

##### Soft blocked

If `nmcli` (`nmcli` command with no arguments) returns something like this :

```
wlan0: unavailable
  "Broadcom BCM43438 combo and Bluetooth Low Energy"
  wifi (brcmfmac), B8:27:EB:95:E0:32, **sw disabled**, hw, mtu 1500
```

Run this :

```bash
rfkill list
```

and ensure it returns `Soft blocked: yes` :

```
0: phy0: Wireless LAN
    Soft blocked: yes
    Hard blocked: no
```

If this is the case, unblock it with this command :

```bash
sudo rfkill unblock wifi
```

and then turn WiFi on with `nmcli` :

```bash
nmcli radio wifi on
```

Finally, to test `nmcli` is working :

```bash
nmcli device wifi list
```

This will return the list of available WiFi networks.

### Using WPA supplicant

Network configuration can be set by editing `/etc/wpa_supplicant/wpa_supplicant.conf` with something similar to this :

```conf
network={
  ssid="Name of your router"
  psk="password"
  key_mgmt=WPA-PSK
  priority=100
}
```

## Linux dependencies for SC RPi

All dependencies listed below are not mandatory but useful for different purposes such as logging and monitoring.

### Glances

[Glances](https://nicolargo.github.io/glances/) is a cross-platform system monitoring tool written in Python. It can be installed through the Python `pip` package manager as described in the [Install](https://glances.readthedocs.io/en/latest/install.html) page of the official documentation, or through `apt-get`.

> It's recommended to install it as a Linux service to start Glances automatically after booting the system. For more information about Linux services, refer to the [Systemd configuration](/doc/linux_for_rapsberry_pi_users#systemd-configuraiton) section in [`/doc/linux_for_rapsberry_pi_users.md`](/doc/linux_for_rapsberry_pi_users.md).

**After installing Glances in the Raspberry Pi, install the [Glances add-on for Home Assistant](/doc/homeassistant.md#glances) to remotely visualize the metrics.**

### Loki

[Grafana Loki](https://grafana.com/docs/loki/latest/), or sometimes abbreviated as Loki, is a logging tool. The [Quick start](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/) explains very well the common Loki-Alloy-Grafana architecture. **For SC RPi it's not necessary to install [Alloy](https://grafana.com/docs/alloy/latest/) nor other tools described in the official page, just Loki is enough.**

Installing Loki with `apt-get` :

1. Add GPG keys for official repos :

    ```bash
    mkdir -p /etc/apt/keyrings/
    wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor > /etc/apt/keyrings/grafana.gpg
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
    ```
2. Update `apt-get` local registries :

    ```bash
    sudo apt-get update
    ```

3. Install `loki` package :
  
    ```bash
    sudo apt-get install loki
    ```

**Additional information:**
- Grafana Loki works only with Raspberry Pi OS 64 bt version.
- Default Loki configuration file is stored in `/etc/loki/config.yml`.
- To check Loki is working correctly open http://raspberrypi.local:3100/ready or http://raspberrypi.local/metrics (replace *raspberrypi.local* with the corresponding hostname).
- To visualize logs remotely, install Grafana and configure the corresponding Grafana Loki datasource in Grafana.
- To install Loki from sources refer to [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5) in Medium. Instead of using `gunzip` for uncompressing, use `unzip`.

## Common issues in Raspberry Pi OS

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

**Transferring code with `rsync`**

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

**Get system architecture**

```bash
uname -m
```

**Get the installed Linux distribution**

```bash
cat /etc/os-release
```

**Disk backup and compression**

```bash
sudo dd if=/dev/diskX bs=4M status=progress | gzip > image.img.gz
```

# Links

- [Connecting with wpa_cli](https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_cli)
- [Glances - Install](https://glances.readthedocs.io/en/latest/install.html)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
- [Grafana Loki](https://grafana.com/docs/loki/latest/)
- [Grafana Loki - Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/)
- [Grafana Loki - Quick start](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/)
- [Query wpa_supplicant with which AP is it associated](https://unix.stackexchange.com/questions/454472/querry-wpa-supplicant-with-which-ap-is-it-associated).
- [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5))
- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
