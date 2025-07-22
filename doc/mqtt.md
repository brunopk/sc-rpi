# MQTT

MQTT (Message Queuing Telemetry Transport) is an application-level protocol, just like HTTP and others, defined around a publish/subscribe architecture (for more information, see the [official MQTT website](https://mqtt.org/)). SC RPi uses MQTT to provide its API and to integrate with Home Assistant. It relies on the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library for working with this protocol in Python.

</br>

> **To work with MQTT, you must have an MQTT broker, which is analogous to a server in HTTP. The recommended broker is Mosquitto (see [Mosquitto broker](#mosquitto-broker) below for more information).**
>
> **For development and troubleshooting, it is also strongly recommended to install [MQTT Explorer](https://mqtt-explorer.com/). It can be installed on macOS using Homebrew, or as a Home Assistant add-on (see the [Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository) and [this post](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5) on the Home Assistant forum).**

</br>

## MQTT integration with HA

SC RPi is integrated with Home Assistant (HA) by listening to specific MQTT topics defined by HA to discover entities and update their states. 

TODO: explain more about topics

</br>

> **Home Assistant provides an official MQTT integration, which must be installed by following [this link](https://my.home-assistant.io/redirect/config_flow_start?domain=mqtt). This will install an HA add-on, which then allows you to install the proper integration. For more information, see the [official MQTT integration documentation](https://www.home-assistant.io/integrations/mqtt/), and specifically the section about [`light`](https://www.home-assistant.io/integrations/light.mqtt/) entities.**

</br>

In Home Assistant jargon, there are different *platforms* for devices, such as `light`, `sensor`, and many others. The MQTT integration provides a mechanism to discover different types of devices and entities. **In this case, SC RPi provides `light` entities.**

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
- [Home Assistant MQTT lights](https://www.home-assistant.io/integrations/light.mqtt/)
- [Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository)
- [Addon MQTT Explorer new Version](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739)
