# Home Assistant

## SC RPi integration with Home Assistant

SC RPi integrates with Home Assistant by creating [`light`](https://www.home-assistant.io/integrations/light.mqtt/) entities through the [MQTT discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery). This mechanism is part of the official [MQTT integration](https://www.home-assistant.io/integrations/mqtt/). To install the MQTT integration follow [this](https://my.home-assistant.io/redirect/config_flow_start?domain=mqtt) link.



> In Home Assistant jargon, there are different *platforms* for devices, such as `light`, `sensor`, and many others. SC RPi generates and provides `light` entities.

### Entities and availability

Each section of the strip is one `light` entity. Its id (the object id) is the section id, for example `section_1`.

Every entity has its own availability topic, set in its discovery message (`availability_topic`):

```text
scrpi/homeassistant/<section id>/availability
```

The payloads are the plain strings `online` and `offline` (Home Assistant's defaults). They are not retained.

At startup, and each time a config is applied (`use_config`, or `reset`), SC RPi publishes, in this order:

1. `offline` for each entity that was running and whose section id is not in the applied config. The entity is only marked unavailable, it is **not** deleted, so its history and UI customization are kept.
2. The discovery message of each section of the applied config (including `availability_topic`).
3. `online` for each section of the applied config.
4. The state of each section (ON/OFF, color and brightness).

At startup there are no previous entities, so there are no `offline` messages.

#### Section ids change when loading another config

Saved configs get their own section ids (`<name>_section_<n>`, see `save_config` in [commands.md](commands.md)). Loading another config therefore replaces the running section ids: entities, automations and history tied to the old ids stop working (the old entities stay as unavailable) and new entities appear for the loaded ids. Applying the same config again (for example `reset` after edits) keeps the ids and sends no `offline` message.

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
- [MQTT Discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)
- [MQTT Explorer - Home Assistant forum thread](https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739/5)
- [MQTT Explorer - Gollum add-on repository for Home Assistant](https://github.com/GollumDom/addon-repository)
- [MQTT Explorer - Official site](https://mqtt-explorer.com/)
