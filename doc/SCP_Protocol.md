# SCP Protocol

It works over TCP and it's a simplification of HTTP. Its main purpose is to manage the communication between [sc-rpi](https://github.com/brunopk/sc-rpi) and [sc-master](https://github.com/brunopk/sc-master). It's mainly implemented on [`src/network.py`](../src/network.py).

## Connection

The only thing to do to establish a connection with [sc-driver](https://github.com/brunopk/sc-driver) using SCP protocol, is to open a TCP connection on port 8080 (defined in [`config.ini`](../config.ini))

## Messages

Similar to HTTP, it has two types of messages: requests and responses. Both, requests and responses are defined as UTF-8 encoded strings containing the JSON stringified representation of a [command](/doc/commands.md).
