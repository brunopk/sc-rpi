# MQTT broker

A known MQTT broker is Mosquitto. It can be installed as an add-on in Home Assistant by following [this](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_mosquitto) link. **It's also recommended to install [MQTT Explorer](https://mqtt-explorer.com/) for development and error troubleshooting (it can be installed in MacOS with Homebrew).**

## HA Mosquito add-on configuration

Go to the add-on configuration page and set the "Logins" field like this :

```yaml
- username: appdaemon
  password: appdaemon
```
