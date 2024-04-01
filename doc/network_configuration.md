# Network configuration

In case of preferring to connect to a WiFi network rather than a wired one, it's recommended to install [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) with **Raspberry Pi Imager** (which may be found [here](https://www.raspberrypi.com/software/)) and set network configuration before writing the OS image to the SD (or USB storage) as shown in [this](https://youtu.be/om8gGB3gyT0?si=OUku24CZW5n7PkQ4&t=31) video. Then, configure [wpa_supplicant](https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_cli) by editing */etc/wpa_supplicant/wpa_supplicant.conf* with something similar to this :

```conf
network={
  ssid="Name of your router"
  psk="password"
  key_mgmt=WPA-PSK
  priority=100
}
```

> For the first boot, and in order to check Raspberry Pi OS starts successfully and connects to the local network, it's recommended to start the system with an HDMI cable connected to a monitor. After that, all commands can be executed through SSH. Also, take into account that it's possible to add multiple SSIDs to the  */etc/wpa_supplicant/wpa_supplicant.conf* with different priorities.

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
