# SCP Protocol

It works over TCP and it's a simplification of HTTP. Its main purpose is to manage the communication between [sc-rpi](https://github.com/brunopk/sc-rpi) and [sc-master](https://github.com/brunopk/sc-master). It's mainly implemented on [`src/network.py`](../src/network.py).

## Connection

To communicate with [sc-rpi](https://github.com/brunopk/sc-rpi), connect to port 8080 (defined in [`config.ini`](../config.ini)) on the host where [sc-rpi](https://github.com/brunopk/sc-rpi) is running. 

## Messages

Similar to HTTP and many protocols, SCP use the concept of requests and responses. Both, requests and responses are defined as UTF-8 encoded strings containing the JSON stringified representation of a [command](/doc/commands.md).
