# Home Assistant

## SC RPi integration with Home Assistant

SC RPi integrates with Home Assistant by creating [`light`](https://www.home-assistant.io/integrations/light.mqtt/) entities through the [MQTT discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery). This mechanism is part of the official [MQTT integration](https://www.home-assistant.io/integrations/mqtt/). To install the MQTT integration follow [this](https://my.home-assistant.io/redirect/config_flow_start?domain=mqtt) link.



> In Home Assistant jargon, there are different *platforms* for devices, such as `light`, `sensor`, and many others. SC RPi generates and provides `light` entities.

## Required apps

### Mosquitto broker

#### Installation

To install Mosquitto broker add-on:

1. Follow [this](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_mosquitto) link
2. Set your Home Assistance URL
3. Click "Open link"

#### Configuration

Go to the add-on configuration page and set the "Logins" field like this :

```yaml
- username: appdaemon
  password: appdaemon
```

### Grafana

Refer to [Grafana app for Home Assistant](https://github.com/hassio-addons/addon-grafana).

## Optional apps

### Glances

It's optional but recommended to install the [Glances add-on for Home Assistant](https://github.com/hassio-addons/addon-glances) to visualize [Glances](https://nicolargo.github.io/glances/) metrics.

### MQTT Explorer

For development and troubleshooting, it is also strongly recommended to install [MQTT Explorer](https://mqtt-explorer.com/). It can be installed on macOS using Homebrew, or as a Home Assistant add-on (see the [Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository) and [this](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5) post on the Home Assistant forum).

## Links

- [Glances - App for Home Assistant](https://github.com/hassio-addons/addon-glances)
- [Glances - Official site](https://nicolargo.github.io/glances/)
- [Grafana - App for Home Assistant](https://github.com/hassio-addons/addon-grafana)
- [Home Assistant - MQTT Discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)
- [MQTT Explorer - Home Assistant forum thread](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5)
- [MQTT Explorer - Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository)
- [MQTT Explorer - Official site](https://mqtt-explorer.com/)
- [Mosquitto broker](/doc/mqtt.md#mosquitto-broker)
