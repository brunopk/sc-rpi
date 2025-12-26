# Home Assistant

## SC RPi integration with Home Assistant

Home Assistant provides an official [MQTT integration](https://www.home-assistant.io/integrations/mqtt/), that can be installed by following [this](https://my.home-assistant.io/redirect/config_flow_start?domain=mqtt) link. This will install an HA add-on, which then allows you to install the proper integration.

SC RPi provides [`light`](https://www.home-assistant.io/integrations/light.mqtt/) entities for Home Assistant through [discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery).

> In Home Assistant jargon, there are different *platforms* for devices, such as `light`, `sensor`, and many others. SC RPi generates and provides `light` entities.

For more information about how SC RPi integrates with Home Assistant see also [`/doc/commands.md`](/doc/commands.md).

## Required add-ons

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

## Optional add-ons

### Glances

It's optional but recommended to install the [Glances add-on for Home Assistant](https://github.com/hassio-addons/addon-glances) to visualize [Glances](https://nicolargo.github.io/glances/) metrics.

### Grafana

It's optional but recommended to install the [Grafana add-on for Home Assistant](https://github.com/hassio-addons/addon-grafana).

### MQTT Explorer

For development and troubleshooting, it is also strongly recommended to install [MQTT Explorer](https://mqtt-explorer.com/). It can be installed on macOS using Homebrew, or as a Home Assistant add-on (see the [Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository) and [this](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5) post on the Home Assistant forum).

## Links

- [Glances - Add-on for Home Assistant](https://github.com/hassio-addons/addon-glances)
- [Glances - Official site](https://nicolargo.github.io/glances/)
- [Grafana - Add-on for Home Assistant](https://github.com/hassio-addons/addon-grafana)
- [Home Assistant - MQTT Discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)
- [MQTT Explorer - Home Assistant forum thread](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5)
- [MQTT Explorer - Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository)
- [MQTT Explorer - Official site](https://mqtt-explorer.com/)
- [Mosquitto broker](/doc/mqtt.md#mosquitto-broker)
