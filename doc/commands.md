# Commands

The API consists of commands transmitted via JSON-formatted messages over a [WebSocket](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/) connection. All commands have the same format :

```json
{
  "name": "command_name",
  "args": {}
}
```

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
- `args` it's another JSON object.
- Colors are represented in hexadecimal.

## disconnect

Close the connection.

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
  "command": "reset"
}
```
  
## status

Return information of the current status of the system.

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

Turn on specific sections or the whole strip

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

Turn off specific sections or the whole strip

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

Change attributes of a section (see `section_new`).

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

Define a new section.

### Example
  
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

Remove sections by id.

### Example
  
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
