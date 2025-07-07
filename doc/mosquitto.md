# Mosquito broker

The MQTT broker can be installed as an add-on in Home Assistant by following [this](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_mosquitto) link.

> It's recommended to install [MQTT Explorer](https://mqtt-explorer.com/) for development and error troubleshooting. It can be installed in MacOS with Homebrew.

## Mosquito broker configuration

Go to the add-on configuration page and set the "Logins" field like this :

```yaml
- username: appdaemon
  password: appdaemon
```
