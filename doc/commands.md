# Commands

Commands are represented as stringified JSONs and sent in the body section of the [SCP protocol](/doc/SCP_Protocol.md), so this is an example of a wrong command representation:

`{"name": "set_color"}` 

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
- reset
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

## `reset`

- What it does: removes all sections.
- Example:
    ```json
    {
      "name": "reset"
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


## `section_edit`

- What it does: changes attributes of a section (see `section_new`).
- Required arguments:
    - `id` : id of the section to edit
- Example 1:
    ```json
    {
      "name": "edit_section",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000",
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
 - Example 2:
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
 - Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {}
    }
    ```
- Example 3:
    ```json
    {
      "name": "edit_section",
      "args": {
        "section_id": "123e4567-e89b-12d3-a456-426614174000",
        "color": "#abc123"
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
  
## `section_add`

- What it does: defines a new section (portion of the strip).
- Example:
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
- Returns: 
    ```json
    {
      "status": 200, 
      "message": "OK", 
      "result": {
          "sections": [
            "0a4e9568-940f-11eb-8de4-b827eb95e032", 
            "0a4ea54e-940f-11eb-8de4-b827eb95e032"
          ]
      }
    }
    ```
  
## `section_remove`

- What it does: removes specific sections by id (or all sections).
- Example:
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
- Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {}
    }
    ```

## `status`

- What it does: returns information of the current status of the system.
- Example:
    ```json
    {
      "name": "status"
    }
    ```
- Returns: 
    ```json
    {
      "status": 200,
      "message": "OK",
      "result": {
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
