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

Returns a configuration, with the same structure as a saved configuration file. Without `name` it returns the **running** configuration: the boot settings with the current sections (including edits, sections turned off and a loaded `use_config`) and description. With `name` it returns the saved configuration `config/<name>.yaml` without applying it; the strip and the running sections are not changed.

Secret values (currently the MQTT password) are replaced by `********`. Every other value is returned as it is.

Arguments:

- `name` (optional): name of a saved configuration.

> **Breaking change:** the payload keys now follow the configuration file: `mqtt_config` is `mqtt` (and its `broker_config` is `broker`), and `strip_config` is `strip`. Sections now include `color` and `is_on`, and the payload includes `description`.

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

Errors (only when `name` is given):

| `status` | `code`                | When                                           |
| -------- | --------------------- | ---------------------------------------------- |
| 400      | `INVALID_CONFIG_NAME` | `name` has characters other than letters, digits, `-`, `_` |
| 404      | `CONFIG_NOT_FOUND`    | no saved configuration has that name           |
| 500      | `INVALID_CONFIG`      | the file cannot be parsed                      |

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

Apply `config/default.yaml` (the boot configuration), or the saved configuration `name` when given. It works like [`use_config`](#use_config) (same validation, errors and Home Assistant updates), so edits and sections turned off are discarded.

Arguments:

- `name` (optional): name of a saved configuration. Defaults to `default`.

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
    ]
  }
}
```

Errors: see [`use_config`](#use_config) (only applicable when `name` is given, except `INVALID_CONFIG`, which also applies to `default`).

## `status`

Return information of the current status of SC RPI.

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
    }]
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

The previous Home Assistant entities are marked unavailable (`offline`, not deleted) and entities for the loaded sections are published and marked available. The result is identical to `reset` with the same `name`, except for `command_name`.

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
        "id": "night_1",
        "start": 0,
        "end": 9,
        "color": { "r": 0, "g": 255, "b": 0 },
        "is_on": false
      }
    ]
  }
}
```

Errors (the strip is left unchanged):

| `status` | `code`                | When                                                                 |
| -------- | --------------------- | -------------------------------------------------------------------- |
| 400      | `MISSING_CONFIG_NAME` | `name` is missing                                                    |
| 400      | `INVALID_CONFIG_NAME` | `name` has characters other than letters, digits, `-`, `_`           |
| 404      | `CONFIG_NOT_FOUND`    | no saved configuration has that name                                 |
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
