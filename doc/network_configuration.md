# Network configuration

To easily run the server and allow other hosts to connect, its recommended to connect it with a prefixed wireless access point or router, or through a wired connection. If it will be connected to through a wired connection there is nothing more to do. In other case, to connect the server to a WiFi network its recommended
to [wpa_supplicant]((https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_cli) which is normally provided with Raspbian.

**The most important is to configure /etc/wpa_supplicant/wpa_supplicant.conf in order to allow Raspbian to automatically connect with your preferred access point or router. This file lists more than one devices each of them with a defined priority to connect :**

```conf
network={
  ssid="Name of your router"
  psk="password"
  key_mgmt=WPA-PSK
  priority=100
}
```

To check to which device is the Raspberry connected:

```bash
iw wlan0 link
```

```bash
iwconfig wlan0
```

```bash
wpa_cli -i wlan0 STATUS   
```

## Links

- [Querry wpa_supplicant with which AP is it associated](https://unix.stackexchange.com/questions/454472/querry-wpa-supplicant-with-which-ap-is-it-associated).
