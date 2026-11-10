# Commands

[MQTT](https://mqtt.org/) (Message Queuing Telemetry Transport) is an application-level protocol, just like HTTP and others, defined around a publish/subscribe architecture. SC RPi uses MQTT to provide its API and to integrate with Home Assistant. It relies on the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library for working with this protocol in Python.

Commands are received from Home Assistant or directly from an MQTT client library such as [Paho](https://pypi.org/project/paho-mqtt/) or using an MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/). SC RPi is integrated with Home Assistant by listening to specific MQTT topics that are defined with the **[MQTT discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)**. Some of the most important topics to interact with Home Assistant are these:

- **Home Assistant command topic**
- **State topic**

Home Assistant requires to define one command topic for each entity. **Additionally, there some specific topics to interact with SC RPi directly:**

- **SC RPi command topic: `scrpi/command`**
- **SC RPi result topic: `scrpi/result`**

Note that there's **one** command topic for all sections in the strip (see [`/src/sc_rpi/utils/topics.py`](/src/sc_rpi/utils/topics.py)). The result topic is for both, successful and failed SC RPi command execution results. Commands sent through the SC RPi command topic have the same format:

```json
{
  "command_name": "command_name",
  "command_args": {}
}
```

All commands, **from user or from Home Assistant**, will return a result through the **result topic** with this format :

```json
{
    "status": 201,
    "command_name": "command_name"
}
```

An example of a failed command result is this:

```json
{
    "status": 400,
    "command_name": "command_name",
    "error": {
      "code": "ALREADY_ON",
      "description": "Section already on"
    }
}
```

**Notes for commands and results :**

- All messages, to/from SC RPi and Home Assistant, are **JSON-formatted** messages.
- Colors are represented as an array of three values (RGB).

**Notes for commands :**

- `args` is a JSON object.

**Notes for results :**

- `payload` and `error` are JSON objects.
- `status` is an integer that adheres to the same semantics as in HTTP.
- `code` is the error code (string).
- Successful SC RPi results will have a `payload` field.
- Failed command messages will have an `error` field (instead of `payload`).

## `edit_section`

Change attributes of a section.

Required arguments:

- `section_id` : id of the section to edit (string)

### Example 1
  
```json
{
  "command_name": "edit_section",
  "command_args": {
    "section_id": "section_1",
    "end": 40
  }
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "edit_section",
  "payload": {
    "sections": [{
        "id": "section_1",
        "start": 0,
        "end": 40,
        "color": [255, 0, 0],
        "is_on": true
      }, {
        "id": "section_2",
        "start": 150,
        "end": 299,
        "color": [0, 255, 0],
        "is_on": true
    }]
  }
}
```

### Example 2
  
```json
{
  "command_name": "edit_section",
  "command_args": {
    "section_id": "section_1",
    "end": 40,
    "start": 10
  }
}
```
  
Returns:

```json
{
  "status": 201,
  "command_name": "edit_section",
  "data": {
    "sections": [{
        "id": "section_1",
        "start": 10,
        "end": 40,
        "color": [255, 0, 0],
        "is_on": true
      }, {
        "id": "section_2",
        "start": 150,
        "end": 299,
        "color": [0, 255, 0],
        "is_on": true
    }]
  }
}
```

### Example 3
  
```json
{
  "command_name": "edit_section",
  "command_args": {
    "section_id": "section_1",
    "color": [123, 123, 123]
  }
}
```

Returns:
  
```json
{
  "status": 201,
  "command_name": "edit_section",
  "data": {
    "sections": [{
        "id": "section_1",
        "start": 10,
        "end": 40,
        "color": [123, 123, 123],
        "is_on": true
      }, {
        "id": "section_2",
        "start": 150,
        "end": 299,
        "color": [0, 255, 0],
        "is_on": true
    }]
  }
}
```

## `get_config`

Returns the saved configuration `config/<name>.yaml`, with the same structure as the file, without applying it: the strip and the running sections are not changed and no file is modified. Secret values (e.g. MQTT password) are replaced by `********`.

To see the running state of the strip, use [`status`](#status).

Arguments:

- `name` (required): name of a saved configuration (letters, digits, `-` and `_`, 1 to 64 characters).

### Example

```json
{
  "command_name": "get_config",
  "command_args": { "name": "party" }
}
```

Returns (shortened to one section):

```json
{
  "status": 202,
  "command_name": "get_config",
  "payload": {
    "connection_timeout": 0.25,
    "default_gateway": "192.168.0.1",
    "default_network_interface": "en0",
    "env": "dev",
    "log_level": "DEBUG",
    "mqtt": {
      "broker": {
        "host": "homeassistant.local",
        "password": "********",
        "port": 1883,
        "username": "test"
      }
    },
    "status_led": 17,
    "strip": {
      "brightness": 255,
      "channel": 0,
      "default_section_brightness": 100,
      "dma": 10,
      "freq_hz": 800000,
      "invert": false,
      "pin": 18,
      "strip_length": 300,
      "sections": [
        {
          "color": { "r": 0, "g": 255, "b": 0 },
          "end": 9,
          "id": "p1",
          "is_on": true,
          "name": "P1",
          "start": 0
        }
      ]
    },
    "description": "Friday lights"
  }
}
```

Errors:

| `status` | `code`                | When                                                       |
|----------|-----------------------|------------------------------------------------------------|
| 400      | `MISSING_CONFIG_NAME` | `name` is missing                                          |
| 400      | `INVALID_CONFIG_NAME` | `name` has characters other than letters, digits, `-`, `_` |
| 404      | `CONFIG_NOT_FOUND`    | no saved configuration has that name                       |
| 500      | `INVALID_CONFIG`      | the file cannot be parsed                                  |

## `help`

Return available commands.

### Example

```json
{
  "command_name": "help"
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "help",
  "payload": {
    "commands": [
      "command_1",
      "command_2"
    ]
  }
}
```

## `reset`

Reload the **active configuration** (the one last loaded by `use_config` or a `reset` with a `name`; `default`, that is `config/default.yaml`, until one is loaded), or apply the saved configuration `name` when given. It works like [`use_config`](#use_config) (same validation, errors and Home Assistant updates), so edits and sections turned off are discarded. A `reset` with a `name` makes that name the active configuration.

The result has the same `payload` as [`status`](#status) right after the command.

Arguments:

- `name` (optional): name of a saved configuration. Defaults to the active configuration.

### Example

```json
{
  "command_name": "reset"
}
```

Returns (for a default configuration with one section):

```json
{
  "status": 202,
  "command_name": "reset",
  "payload": {
    "sections": [
      {
        "id": "section_1",
        "start": 0,
        "end": 99,
        "color": { "r": 0, "g": 255, "b": 0 },
        "is_on": true
      }
    ],
    "active_configuration": "default",
    "description": ""
  }
}
```

Errors: see [`use_config`](#use_config) (`MISSING_CONFIG_NAME` does not apply). Without `name`, `CONFIG_NOT_FOUND` and `INVALID_CONFIG` refer to the active configuration's file (for example if it was deleted or edited by hand); the strip, the sections and the active configuration are left unchanged.

## `save_config`

Save the running configuration (sections with their range, color and on/off state, plus the description) as `config/<name>.yaml`, so it can be loaded later with [`use_config`](#use_config) or [`reset`](#reset). The `.yaml` extension is added by SC RPi and is not part of `name`.

- An existing saved configuration is only replaced when `overwrite` is `true`; otherwise saving with a name that is already taken fails with `CONFIG_ALREADY_EXISTS` and the file is left unchanged. The replacement is atomic: the file holds either the old or the new complete content.
- When `name` is omitted, the **active configuration's** name is used, as if it had been given. Saving your edits back to the active configuration therefore needs `overwrite` `true`, and it is rejected with `RESERVED_CONFIG_NAME` while `default` is active (for example right after startup).
- `default` is reserved (compared case-insensitively, so `Default` and `DEFAULT` are rejected too, even with `overwrite`) and the initial configuration `config/default.yaml` is never modified.
- The active configuration is not changed by `save_config`.
- Sections are saved with the ids and names they have, ordered by `start`.
- The saved file keeps the real MQTT password (it must be a valid configuration); the result shows it masked.
- The strip is not re-rendered, no section changes and no Home Assistant message is published.

Arguments:

- `name` (optional): name for the saved configuration (letters, digits, `-` and `_`, 1 to 64 characters). Defaults to the active configuration's name.
- `description` (optional): a text description of the configuration (default: empty string).
- `overwrite` (optional): `true` to replace an existing saved configuration (default: `false`).

### Example

```json
{
  "command_name": "save_config",
  "command_args": { "name": "party", "description": "Friday night lights" }
}
```

Returns (shortened to one section). The `payload` is the saved configuration, exactly the same as the [`get_config`](#get_config) payload for that name:

```json
{
  "status": 202,
  "command_name": "save_config",
  "payload": {
    "connection_timeout": 0.25,
    "default_gateway": "192.168.0.1",
    "default_network_interface": "en0",
    "env": "dev",
    "log_level": "DEBUG",
    "mqtt": {
      "broker": {
        "host": "homeassistant.local",
        "password": "********",
        "port": 1883,
        "username": "test"
      }
    },
    "status_led": 17,
    "strip": {
      "brightness": 255,
      "channel": 0,
      "default_section_brightness": 100,
      "dma": 10,
      "freq_hz": 800000,
      "invert": false,
      "pin": 18,
      "strip_length": 300,
      "sections": [
        {
          "color": { "r": 0, "g": 255, "b": 0 },
          "end": 9,
          "id": "desk",
          "is_on": true,
          "name": "Desk",
          "start": 0
        }
      ]
    },
    "description": "Friday night lights"
  }
}
```

Errors (nothing is changed and no file is written):

| `status` | `code`                  | When                                                                                              |
|----------|-------------------------|---------------------------------------------------------------------------------------------------|
| 400      | `INVALID_CONFIG_NAME`   | `name` has characters other than letters, digits, `-`, `_`                                        |
| 400      | `RESERVED_CONFIG_NAME`  | the name used (given, or the active one) is `default` (in any letter case), also with `overwrite` |
| 409      | `CONFIG_ALREADY_EXISTS` | a saved configuration with that name already exists and `overwrite` is not `true`                 |

## `status`

Return information of the current status of SC RPI: the running sections, the name of the **active configuration** (the one [`reset`](#reset) without a `name` reloads; `default` after startup) and the running description. The active configuration is kept in memory only, so after a restart it is `default` again.

### Example
  
```json
{
  "command_name": "status"
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "status",
  "payload": {
    "sections": [{
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "start": 150,
        "end": 299,
        "color": "#00ff00",
        "is_on": true
    }],
    "active_configuration": "default",
    "description": ""
  }
}
```

## `turn_section_off`

Turn off specific sections or the whole strip

### Example 1
  
```json
{
  "command_name": "turn_section_off"
}
```

### Example 2

```json
{
  "command_name": "turn_off",
  "command_args": {
    "section_id": "section_1"
  }
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "turn_section_off",
  "data": {
    "sections": [{
          "id": "section_1",
          "start": 0,
          "end": 149,
          "color": [255, 0, 0],
          "is_on": false
        }, {
          "id": "section_2",
          "start": 150,
          "end": 299,
          "color": [0, 255, 0],
          "is_on": true
    }]
  }
}
```

## `turn_section_on`

Turn on specific sections or the whole strip

### Example 1

```json
{
  "command_name": "turn_section_on",
  "command_args": {
    "section_id": "section_1"
  }
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "turn_section_on",
  "data": {
    "sections": [{
          "id": "section_1",
          "start": 0,
          "end": 149,
          "color": [255, 0, 0],
          "is_on": true
        }, {
          "id": "section_2",
          "start": 150,
          "end": 299,
          "color": [0, 255, 0],
          "is_on": true
    }]
  }
}
```

### Example 2

```json
{
  "command_name": "turn_section_on",
  "command_args": {
    "section_id": "section_1",
    "color": [123, 123, 123]
  }
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "turn_section_on",
  "data": {
    "sections": [{
          "id": "section_1",
          "start": 0,
          "end": 149,
          "color": [123, 123, 123],
          "is_on": true
        }, {
          "id": "section_2",
          "start": 150,
          "end": 299,
          "color": [0, 255, 0],
          "is_on": true
    }]
  }
}
```

## `use_config`

Apply the saved configuration `config/<name>.yaml` immediately. Sections (ranges, colors, on/off state) and the description are replaced and the strip is re-rendered. Hardware (strip) and MQTT settings of the loaded file are **not** applied, and no file in `config/` is modified.

The previous Home Assistant entities are marked unavailable (`offline`, not deleted) and entities for the loaded sections are published and marked available.

On success `name` becomes the **active configuration** (the one [`reset`](#reset) without a `name` reloads); on failure it is unchanged. It is kept in memory only, so after a restart it is `default` again.

Arguments:

- `name` (required): name of a saved configuration (letters, digits, `-` and `_`, 1 to 64 characters).

### Example

```json
{
  "command_name": "use_config",
  "command_args": { "name": "night" }
}
```

Returns:

```json
{
  "status": 202,
  "command_name": "use_config",
  "payload": {
    "sections": [
      {
        "id": "night_section_1",
        "start": 0,
        "end": 9,
        "color": { "r": 0, "g": 255, "b": 0 },
        "is_on": false
      }
    ],
    "active_configuration": "night",
    "description": ""
  }
}
```

Errors (the strip is left unchanged):

| `status` | `code`                | When                                                                  |
|----------|-----------------------|-----------------------------------------------------------------------|
| 400      | `MISSING_CONFIG_NAME` | `name` is missing                                                     |
| 400      | `INVALID_CONFIG_NAME` | `name` has characters other than letters, digits, `-`, `_`            |
| 404      | `CONFIG_NOT_FOUND`    | no saved configuration has that name                                  |
| 500      | `INVALID_CONFIG`      | the file cannot be parsed, or a section overlaps or exceeds the strip |

## `version`

### Example
  
```json
{
  "command_name": "version"
}
```

Returns :

```json
{
  "status": 202,
  "command_name": "version",
  "payload": {
      "python_version": "3.8.18",
      "sc_rpi_version": "0.1.0"
  }
}
```

## Links

- [A Beginner’s Guide to MQTT: Understanding MQTT, Mosquitto Broker, and Paho Python MQTT Client](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923)
- [Home Assistant - MQTT Discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)
- [MQTT Explorer - Official site](https://mqtt-explorer.com/)
- [MQTT protocol - Official site](https://mqtt.org/)
- [Paho](https://pypi.org/project/paho-mqtt/)
