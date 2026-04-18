# Linux services

To initiate SC RPi as a [linux service](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/#managing-services) follow these steps:

1. Create the service configuration in `/etc/systemd/system/sc-rpi.service` with something like this:

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

   Python interpreter (`/home/pi/sc-rpi/.direnv/bin/python`) should point to the Python interpreter created for the virtual environment.
   <br></br>

2. Enable the service :

   ```bash
   systemctl enable sc-rpi.service
   ```
   
   The service name, in this case `sc-rpi.service`, must match with service configuration file name (i.e. `/etc/systemd/system/sc-rpi.service`).
   <br></br>

3. Start the service :

   ```bash
   systemctl start sc-rpi.service
   ```

Refer to the [Useful commands](#useful-commands) section for useful commands to work with Linux services.

# Network configuration

There're many ways to configure network in Linux :

- [Using Network Manager](#using-network-manager)
- [Using WPA supplicant (through configuration files)](#using-wpa-supplicant)

</br>

**The preferred way to configure the network in Raspbian OS is using Network Manager.**

**To check to which device is the Raspberry connected :**

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

**It may be necessary to run these commands with `sudo`.**

## Using Network Manager

To connect to a WiFi network :

```bash
sudo nmcli device wifi connect "YourSSID" --ask
```

To discover WiFi networks (with or without `sudo`):

```bash
nmcli device wifi list
```

**Using Network Manager with Raspbian GNU/Linux 11 (Bullseye)**

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

**Common errors**

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

## Using WPA supplicant

Network configuration can be set by editing `/etc/wpa_supplicant/wpa_supplicant.conf` with something similar to this :

```conf
network={
  ssid="Name of your router"
  psk="password"
  key_mgmt=WPA-PSK
  priority=100
}
```

# Complementary software for SC RPi

All dependencies listed below are not mandatory but useful for different purposes such as logging and monitoring.

## Glances

[Glances](https://nicolargo.github.io/glances/) is a cross-platform system monitoring tool written in Python. It can be installed through the Python `pip` package manager as described in the [Install](https://glances.readthedocs.io/en/latest/install.html) page of the official documentation, or through `apt-get`.

**After installing Glances in the Raspberry Pi, install the [Glances add-on for Home Assistant](/doc/homeassistant.md#glances) to remotely visualize the metrics.**

# Alloy

As described in its official documentation, Grafana Alloy is an open source telemetry collector for metrics, logs, traces, and continuous profiles. As explained in the [Quickstart to run Loki locally](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/#quickstart-to-run-loki-locally), Alloy is part of a big architecture often built with Docker, but for SC RPi its enough to install Alloy and Loki as Linux services in the Raspberry Pi as there's no Loki and Alloy apps for Home Assistant. To install and configure Alloy follow these steps : 


1. Add GPG keys for official repos (if not done before) and update `apt-get` registries as described in the [Loki](#loki) section.
2. Add this configuration to `/etc/alloy/config.alloy`: 

   ```
   loki.source.journal "read" {
     forward_to = [loki.process.parse_logs.receiver]
     matches    = "_SYSTEMD_UNIT=sc-rpi.service"
     labels     = {service = "sc-rpi"}
   }

   loki.process "parse_logs" {
     forward_to = [loki.write.endpoint.receiver]

     stage.logfmt {
       mapping = {
         level = "level",
         msg = "event",
       }
     }

     stage.labels {
       values = {
       level = "",
     }
   }

   loki.write "endpoint" {
     endpoint {
       url = "http://localhost:3100/loki/api/v1/push"
     }
   }
   ```
3. Enable the service (if it is not enabled yet):

   ```bash
   systemctl enable alloy
   ```
4. Start the service :

   ```bash
   systemctl start alloy
   ```

**Important :**   
- Alloy must be installed after Loki

**Additional information :**
- To verify that Alloy is running :
   1. Add this configuration to `/etc/default/alloy` :
         ```
         # User-defined arguments to pass to the run command.
         CUSTOM_ARGS="--server.http.listen-addr=0.0.0.0:12345"
         ```
   2. Restart the service
   3. Open http://raspberrypi.local:12345 (replace *raspberrypi.local* with the corresponding hostname) 
- The instructions to install Alloy described above were extracted from https://apt.grafana.com/, Refer to the [Install](https://grafana.com/docs/alloy/latest/set-up/install/linux/#install) section of the official documentation for more information.



## Loki

[Grafana Loki](https://grafana.com/docs/loki/latest/), or sometimes abbreviated as Loki, is a logging tool. The [Quick start](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/) explains very well the common Loki-Alloy-Grafana architecture. To install Loki with `apt-get` follow these steps : 

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

**Important :**   
- Loki must be installed before Alloy

**Additional information :**
- The instructions to install Loki described above were extracted from https://apt.grafana.com/. Refer also to the [Install using APT or RPM package manager
](https://grafana.com/docs/loki/latest/setup/install/local/#install-using-apt-or-rpm-package-manager) section for more information.
- Grafana Loki works only with Raspberry Pi OS 64 bt version.
- Default Loki configuration file is stored in `/etc/loki/config.yml`.
- To check Loki is working correctly open http://raspberrypi.local:3100/ready or http://raspberrypi.local/metrics (replace *raspberrypi.local* with the corresponding hostname).
- To visualize logs remotely, install Grafana and configure the corresponding Grafana Loki datasource in Grafana.

# Common issues in Raspberry Pi OS

In case SSH is not working, check if `ssh.service` is correctly enabled :

```bash
systemctl status ssh.service
```

If necessary enable it with `systemctl` :

```bash
systemctl enable ssh.service
```

> It may be necessary to run `systemctl` with `sudo`

# Useful commands

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

**To check if a service is working correctly :**

```bash
systemctl status sc-rpi.service
```

**To restart a service :**

```bash
systemctl restart sc-rpi.service
```

**To reload a service after changing its unit file :**

```bash
systemctl daemon-reload
```

**To get service logs :**

```bash
journalctl -u sc-rpi.service
```

# Links

- [Connecting with wpa_cli](https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_cli)
- [Glances - Install](https://glances.readthedocs.io/en/latest/install.html)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
- [Grafana Loki](https://grafana.com/docs/loki/latest/)
- [How To Use journalctl to View and Manipulate systemd Logs on Linux](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)
- [Query wpa_supplicant with which AP is it associated](https://unix.stackexchange.com/questions/454472/querry-wpa-supplicant-with-which-ap-is-it-associated).
- [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5))
- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
- [What is Systemctl? An In-Depth Overview](https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview)
