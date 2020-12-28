# SCP Protocol

It works over TCP and it's a simplification of HTTP. Its main purpose is to manage the communication between [sc-driver](https://github.com/brunopk/sc-driver) and [sc-master](https://github.com/brunopk/sc-master). It's mainly implemented on [`src/network.py`](../src/network.py).

## Connection

The only thing to do to establish a connection with [sc-driver](https://github.com/brunopk/sc-driver) using SCP protocol, is to open a TCP connection on port 8080 (defined in [`config.ini`](../config.ini))

## Messages

Similar to HTTP, it has two types of messages: requests and responses. Both, requests and responses are defined as UTF-8 encoded strings with two sections :

- Headers
- Body


### Headers:

Headers section MUST follow this pattern for each header line:

`<HEADER_NAME>: <VALUE><CARRIAGE_RETURN><END_OF_LINE>`

respecting this simple rules :

- It's all case-sensitive
- Between `<HEADER_NAME>:` and `<VALUE>` there's a space (`\s` character)

Currently there's one possible header:

`Content-Length: <VALUE>` 

where `<VALUE>` represents the command length in bytes with NO MORE than 7 digits.
           

### Body:


Contains the JSON representation of the [command](/doc/commands.md).