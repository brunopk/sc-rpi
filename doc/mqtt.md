# MQTT

**To work with MQTT, it's very useful to have [MQTT Explorer](https://mqtt-explorer.com/). It can be installed on macOS using Homebrew. This application is extremely helpful for development and troubleshooting.**

## MQTT integration with HA

Home Assistant provides an official integration for MQTT which can be installed by following [this](https://my.home-assistant.io/redirect/config_flow_start?domain=mqtt) link. But, as described in the [official documentation of the MQTT integration](https://www.home-assistant.io/integrations/mqtt/), **the first step to get MQTT and Home Assistant working is to choose a broker** (see also [Mosquitto broker](#mosquitto-broker) below).

The MQTT integration provides a mechanism to discover devices and entities. [This](https://www.home-assistant.io/integrations/light.mqtt/) part of the official documentation explains how to make Home Assistant discover `light` entities (in Home Assistant jargon, there are different "platforms" for devices, such as `light` and `sensor`, among many others) and describes the format of the messages. **SC RPi sends MQTT messages in JSON format.**

## Mosquitto broker

HA is provided with an official add-on to run a **MQTT broker**, which can be installed by following [this](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_mosquitto) link.

### Mosquitto broker configuration

Go to the add-on configuration page and set the "Logins" field like this :

```yaml
- username: appdaemon
  password: appdaemon
```

## Links

- [Official MQTT protocol site](https://mqtt.org/)
- [Home Assistant MQTT integration](https://www.home-assistant.io/integrations/mqtt/)
