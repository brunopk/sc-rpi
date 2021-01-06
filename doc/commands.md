# Commands

Commands are represented as stringified JSONs and sent in the body section of the [SCP protocol](/doc/SCP_Protocol.md), so this is an example of a wrong command representation:

`{"name": "set_color"` 

And this is an example of a good command representation:

`{"name": "set_color"}`

All commands MUST follow this schema:

```json
{
  "name": "COMMAND_NAME",
  "args": "COMMAND_ARGUMENTS"
}
```

where `<COMMAND_NAME>` is a string and `<COMMAND_ARGUMENTS>` it's an objecy.

They are defined and implemented on the [`src/commands/`](../src/commands) directory. Currently the available commands (command names) are: 

- disconnect
- edit_section
- new_section
- set_color


## `disconnect`

- What it does: closes the TCP connection.
- Example:
    ```json
    {
      "name": "disconnect"
    }
    ```
- Returns: nothing


## `edit_section`

- What it does: changes attributes of a section (see `new_section`).
- Example:
    ```json
    {
      "name": "edit_section",
      "args": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "end": 40
      }
    }
    ```
 - Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {}
    }
    ```
  
## `new_section`

- What it does: defines a new section (portion of the strip).
- Example:
    ```json
    {
      "name": "new_section",
      "args": {
        "start": 1,
        "end": 50
      }
    }
    ```
- Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {
        "id": "123e4567-e89b-12d3-a456-426614174000"        
      }
    }
    ```
  
## `set_color`

- What it does: changes color for all the LEDs or for LEDs in a specific section (see `new_section`).
- Example:
    ```json
    {
      "name": "set_color",
      "args": {
        "section": "123e4567-e89b-12d3-a456-42661417400",
        "color": "#AABBCC"
      }
    }
    ```
- Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {}
    }
    ```
