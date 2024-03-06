# Commands

The API for sc-rpi consist of commands sent through [WebSocket](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/) which provides several important features, including bi-directional communication which is particularly important for sc-rpi. Commands are defined and implemented on [`src/commands/`](../src/commands), and represented as JSON objects.

## Commands

Commands are represented as JSON objects with a specific format:

```json
{
  "command": "command_name",
  "args": {}
}
```

where the value for `args` it's another JSON object. **All commands** return responses with the following format :

```json
{
    "status": 201,
    "description": "accepted",
    "data": null
}
```

where :

- `status` : HTTP status codes, commonly 201 (accepted).
- `description`: an string describing more information about response.
- `data`: another object with more information if the command requires it, `null` for most commands

In general for requests and responses :

- Colors are represented in hexadecimal.
- Although the WebSocket protocol itself doesn't natively incorporate status codes like HTTP, sc-rpi is designed to implement and utilize them for responses.

Available commands are : 

- [Commands](#commands)
  - [Commands](#commands-1)
    - [disconnect](#disconnect)
    - [reset](#reset)
    - [status](#status)
    - [turn\_on](#turn_on)
    - [turn\_off](#turn_off)
    - [section\_edit](#section_edit)
    - [section\_add](#section_add)
    - [section\_remove](#section_remove)
  - [Links](#links)

### disconnect

- What it does: closes the TCP connection.
- Example:
  ```json
    {
      "command": "disconnect"
    }
    ```
- Returns: nothing

### reset

- What it does: removes all sections.
- Example:
    ```json
    {
      "command": "reset"
    }
    ```
- Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": null
    }
    ```
  
### status

- What it does: returns information of the current status of the system.
- Example:
    ```json
    {
      "command": "status"
    }
    ```
- Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": {
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

### turn_on

- What it does: turns on specific sections or the whole strip

- Example 1:
    ```json
    {
      "command": "turn_on"
    }
    ```

- Example 2:

    ```json
    {
      "command": "turn_on",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000"
      }
    }
    ```

### turn_off

- What it does: turns off specific sections or the whole strip

- Example 1:
    ```json
    {
      "command": "turn_off"
    }
    ```

- Example 2:

    ```json
    {
      "command": "turn_off",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000"
      }
    }
    ```

### section_edit

- What it does: changes attributes of a section (see `section_new`).
- Required arguments:
    - `id` : id of the section to edit
- Example 1:
    ```json
    {
      "command": "edit_section",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000",
        "end": 40
      }
    }
    ```
 - Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": null
    }
    ```
 - Example 2:
    ```json
    {
      "command": "edit_section",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000",
        "end": 40,
        "start": 10
      }
    }
    ```
 - Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": null
    }
    ```
- Example 3:
    ```json
    {
      "command": "edit_section",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000",
        "color": "#abc123"
      }
    }
    ```
 - Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": null
    }
    ```

### section_add

- What it does: defines a new section.
- Example:
    ```json
    {
      "command": "section_add",
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
- Returns: 
    ```json
    {
      "status": 201, 
      "description": "accepted", 
      "data": {
          "sections": [
            "0a4e9568-940f-11eb-8de4-b827eb95e032", 
            "0a4ea54e-940f-11eb-8de4-b827eb95e032"
          ]
      }
    }
    ```

### section_remove

- What it does: removes sections by id.
- Example:
    ```json
    {
      "command": "section_remove",
      "args": {
        "sections": [
          "123e4567-e89b-12d3-a456-42661417400",
          "123e4567-e89b-12d3-a456-42661417500"
        ]
      }
    }
    ```
- Returns: 
    ```json
    {
      "status": 201,
      "description": "accepted",
      "data": null
    }
    ```

## Links

- [Send WebSocket requests with Postman](https://learning.postman.com/docs/sending-requests/websocket/websocket-overview/)
