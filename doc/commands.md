# Commands

The API consists of commands transmitted via JSON-formatted messages over a [WebSocket](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/) connection. All commands have the same format :

```json
{
  "name": "command_name",
  "args": {}
}
```

where `args` is another JSON (nested) object. **Successful command execution** will return a response with this format :

```json
{
    "status": 201,
    "command": "command_name"
}
```

and optionally a `data` field which is another (nested) JSON object :

```json
{
    "status": 201,
    "command": "command_name",
    "data": {}
}
```

**Failed command execution** will return a response with this format :

```json
{
    "status": 400,
    "command": "command_name",
    "error": {
      "code": "ALREADY_ON"
    }
}
```

where `code` is the error code (string).

In general for requests and responses colors are represented in hexadecimal. **All responses (failure or success) will have a `status` key**, which is an integer that adheres to the same semantics as in HTTP.

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

## help

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
  "command": "help",
  "data": {
    "commands": [
      "command_1",
      "command_2"
    ]
  }
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
  "command": "reset",
  "data": {
    "sections": []
  }
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
  "data": {
    "sections": [{
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "start": 0,
        "end": 149,
        "color": "#ff0000",
        "is_on": true
      }, {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "start": 150,
        "end": 299,
        "color": "#00ff00",
        "is_on": true
    }]
  }
}
```

## section_edit

Change attributes of a section (see `section_new`).

Required arguments:

- `id` : id of the section to edit

### Example 1
  
```json
{
  "name": "section_edit",
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
  "command": "section_edit",
  "data": {
    "sections": [{
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "start": 0,
        "end": 149,
        "color": "#ff0000",
        "is_on": true
      }, {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "start": 150,
        "end": 299,
        "color": "#00ff00",
        "is_on": true
    }]
  }
}
```

### Example 2
  
```json
{
  "name": "section_edit",
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
  "data": {
    "sections": [{
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "start": 10,
        "end": 40,
        "color": "#ff0000",
        "is_on": true
      }, {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "start": 150,
        "end": 299,
        "color": "#00ff00",
        "is_on": true
    }]
  }
}
```

### Example 3
  
```json
{
  "name": "section_edit",
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
  "command": "section_edit",
  "data": {
    "sections": [{
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "start": 10,
        "end": 40,
        "color": "#abc123",
        "is_on": true
      }, {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "start": 150,
        "end": 299,
        "color": "#00ff00",
        "is_on": true
    }]
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
      "123e4567-e89b-12d3-a456-42661417400"
    ]
  }
}
```

Returns:

```json
{
  "status": 201,
  "command": "section_remove",
  "data": {
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
  "command": "turn_off",
  "data": {
    "sections": [{
          "id": "123e4567-e89b-12d3-a456-426614174000",
          "start": 0,
          "end": 149,
          "color": "#ff0000",
          "is_on": false
        }, {
          "id": "123e4567-e89b-12d3-a456-426614174001",
          "start": 150,
          "end": 299,
          "color": "#00ff00",
          "is_on": true
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
  "command": "turn_on",
  "data": {
    "sections": [{
          "id": "123e4567-e89b-12d3-a456-426614174000",
          "start": 0,
          "end": 149,
          "color": "#ff0000",
          "is_on": true
        }, {
          "id": "123e4567-e89b-12d3-a456-426614174001",
          "start": 150,
          "end": 299,
          "color": "#00ff00",
          "is_on": true
    }]
  }
}
```

## version

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
  "data": {
      "python_version": "3.8.18",
      "sc_rpi_version": "0.1.0"
  },
  "command": "version"
}
```

## Links

- [Send WebSocket requests with Postman](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/)
