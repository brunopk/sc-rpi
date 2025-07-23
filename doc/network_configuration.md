# Network configuration

**The preferred way to configure the network in Raspbian OS is using Network Manager (see [Using Network Manager](#using-network-manager) below)**, but it can also be configured with WPA Supplicant (see [Using WPA Supplicant](#using-wpa-supplicant) below).

# Using Network Manager

To connect to a WiFi network :

```bash
sudo nmcli device wifi connect "YourSSID" --ask
```

To discover WiFi networks (with or without `sudo`):

```bash
nmcli device wifi list
```

## Common errors

### Soft blocked

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

### Configuration in Raspbian GNU/Linux 11 (Bullseye)**

</br>

##  Using Network Manager with Raspbian GNU/Linux 11 (Bullseye)

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


# Using WPA supplicant

Network configuration can be set by editing */etc/wpa_supplicant/wpa_supplicant.conf* with something similar to this :

```conf
network={
  ssid="Name of your router"
  psk="password"
  key_mgmt=WPA-PSK
  priority=100
}
```

</br>
</br>

To check to which device is the Raspberry connected:

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

## Links

- [Querry wpa_supplicant with which AP is it associated](https://unix.stackexchange.com/questions/454472/querry-wpa-supplicant-with-which-ap-is-it-associated).
- [Connecting with wpa_cli](https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_cli)
