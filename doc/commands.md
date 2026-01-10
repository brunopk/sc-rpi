# Commands

[MQTT](https://mqtt.org/) (Message Queuing Telemetry Transport) is an application-level protocol, just like HTTP and others, defined around a publish/subscribe architecture. SC RPi uses MQTT to provide its API and to integrate with Home Assistant. It relies on the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library for working with this protocol in Python.

Commands are received from Home Assistant or directly from an MQTT client library such as [Paho](https://pypi.org/project/paho-mqtt/) or using an MQTT client such as [MQTT Explorer](https://mqtt-explorer.com/). SC RPi is integrated with Home Assistant by listening to specific MQTT topics that are defined with the **[MQTT discovery mechanism](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)**. Some of the most important topics to interact with Home Assistant are these:

- **Home Assistant command topic**
- **State topic**

Home Assistant requires to define one command topic for each entity. **Additionally, there some specific topics to interact with SC RPi directly:**

- **SC RPi command topic: `scrpi/command`**
- **Result topic (for successful and failed SC RPi command execution results): `scrpi/result`**

Note that there's **one** command topic for all sections in the strip (see [`/src/sc_rpi/utils/topic_utils.py`](/src/sc_rpi/utils/topic_utils.py)). All messages, to/from SC RPi and Home Assistant, are **JSON-formatted** messages. Commands sent through the SC RPi command topic have the same format:

```json
{
  "name": "command_name",
  "args": {}
}
```

where `args` is another JSON object. All commands execution will return a result through the **result topic** with this format :

```json
{
    "status": 201,
    "command_name": "command_name"
}
```

where `status` is an integer that adheres to the same semantics as in HTTP. Optionally, successful command results will have a **`payload`** field. 

Instead of `payload`, failed command messages will have an **`error`** field. Both, `payload` and `error` are JSON objects. An example of a failed command result is this:

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

where `code` is the error code (string).

> **Colors are represented as an array of three values (RGB).**

## `edit_section`

Change attributes of a section.

Required arguments:

- `section_id` : id of the section to edit (string)

### Example 1
  
```json
{
  "name": "edit_section",
  "args": {
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
  "name": "edit_section",
  "args": {
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
  "name": "edit_section",
  "args": {
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

Returns configuration parameters of SC RPI.

### Example

```json
{
  "name": "get_config"
}
```

Returns:
  
```json
{
  "status": 201,
  "command_name": "get_config",
  "payload": {
    "connection_timeout": 0.25,
    "default_gateway": "192.168.0.1",
    "default_network_interface": "en0",
    "env": "dev",
    "host": "0.0.0.0",
    "strip_config": {
      "invert": false,
      "pin": 18,
      "strip_length": 300
    }
  }
}
```

## `help`

Return available commands.

### Example

```json
{
  "name": "help"
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

Remove all sections.

### Example

```json
{
  "name": "reset"
}
```

Returns:

```json
{
  "status": 201,
  "command_name": "reset",
  "payload": {
    "sections": []
  }
}
```

## `status`

Return information of the current status of SC RPI.

### Example
  
```json
{
  "name": "status"
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
  "name": "turn_section_off"
}
```

### Example 2

```json
{
  "name": "turn_off",
  "args": {
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
  "name": "turn_section_on",
  "args": {
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
  "name": "turn_section_on",
  "args": {
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

## `version`

### Example
  
```json
{
  "name": "version"
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
