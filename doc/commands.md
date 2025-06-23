# Commands

The API consists of commands transmitted via JSON-formatted messages over a [WebSocket](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/) connection. All commands have the same format :

```json
{
  "name": "command_name",
  "args": {}
}
```

where the value for `args` it's another JSON object.

**All commands responses** have the same format :

```json
{
    "status": 201,
    "command": "command_name",
    "payload": {}
}
```

This means that error responses will also follow this format. For example, an error response might look like this:

```json
{
    "status": 400,
    "command": "command_name",
    "payload": {
      "code": "ALREADY_ON"
    }
}
```

In general for requests and responses :

- `status` adheres to the same semantics as HTTP status codes.
- `payload` is another JSON object. In case of errors, It will have a `code` key with the error code (string). It may be `null` for some commands.
- Colors are represented in hexadecimal.

## Table of content

- [Commands](#commands)
  - [Table of content](#table-of-content)
  - [disconnect](#disconnect)
    - [Example](#example)
  - [reset](#reset)
    - [Example](#example-1)
  - [status](#status)
    - [Example](#example-2)
  - [turn\_on](#turn_on)
    - [Example 1](#example-1)
    - [Example 2](#example-2)
  - [turn\_off](#turn_off)
    - [Example 1](#example-1-1)
    - [Example 2](#example-2-1)
  - [section\_edit](#section_edit)
    - [Example 1](#example-1-2)
    - [Example 2](#example-2-2)
    - [Example 3](#example-3)
  - [section\_add](#section_add)
    - [Example:](#example-3)
  - [section\_remove](#section_remove)
    - [Example:](#example-4)
  - [Links](#links)

## disconnect

- What it does: closes the TCP connection.

### Example

```json
{
  "name": "disconnect"
}
```

Returns:
  
```json
{
  "status": 201,
  "command": "disconnect"
}
```

## reset

What it does: removes all sections.

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
  "command": "reset"
}
```
  
## status

What it does: returns information of the current status of the system.

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
  "command": "status",
  "payload": {
    "number_of_led": 300,
    "sections": [{
      "id":  "123e4567-e89b-12d3-a456-42661417400",
      "color": "#AABBCC",
      "limits": {
        "start": 0,
        "end": 100
      }
    }]   
  }
}
```

## turn_on

What it does: turns on specific sections or the whole strip

### Example 1
  
```json
{
  "name": "turn_on"
}
```

### Example 2

```json
{
  "name": "turn_on",
  "args": {
    "section_id": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

Returns:

```json
{
  "status": 201,
  "command": "turn_on"
}
```

## turn_off

What it does: turns off specific sections or the whole strip

### Example 1
  
```json
{
  "name": "turn_off"
}
```

### Example 2

```json
{
  "name": "turn_off",
  "args": {
    "section_id": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

Returns:

```json
{
  "status": 201,
  "command": "turn_off"
}
```

## section_edit

What it does: changes attributes of a section (see `section_new`).
Required arguments:

- `id` : id of the section to edit

### Example 1
  
```json
{
  "name": "edit_section",
  "args": {
    "section_id": "123e4567-e89b-12d3-a456-426614174000",
    "end": 40
  }
}
```

Returns:

```json
{
  "status": 201,
  "command": "section_edit"
}
```

### Example 2
  
```json
{
  "name": "edit_section",
  "args": {
    "section_id": "123e4567-e89b-12d3-a456-426614174000",
    "end": 40,
    "start": 10
  }
}
```
  
Returns:

```json
{
  "status": 201,
  "command": "section_edit",
}
```

### Example 3
  
```json
{
  "name": "edit_section",
  "args": {
    "section_id": "123e4567-e89b-12d3-a456-426614174000",
    "color": "#abc123"
  }
}
```

Returns:
  
```json
{
  "status": 201,
  "command": "section_edit"
}
```

## section_add

What it does: defines a new section.

### Example:
  
```json
{
  "name": "section_add",
  "args": {
    "sections": [{
        "start": 0,
        "end": 149,
        "color": "#ff0000"
      }, {
        "start": 150,
        "end": 299,
        "color": "#00ff00"
    }]
  }
}
```

Returns:
  
```json
{
  "status": 201, 
  "command": "section_add", 
  "payload": {
      "sections": [
        "0a4e9568-940f-11eb-8de4-b827eb95e032", 
        "0a4ea54e-940f-11eb-8de4-b827eb95e032"
      ]
  }
}
```

## section_remove

What it does: removes sections by id.

### Example:
  
```json
{
  "name": "section_remove",
  "args": {
    "sections": [
      "123e4567-e89b-12d3-a456-42661417400",
      "123e4567-e89b-12d3-a456-42661417500"
    ]
  }
}
```

Returns:

```json
{
  "status": 201,
  "command": "section_remove"
}
```

## Links

- [Send WebSocket requests with Postman](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/)
