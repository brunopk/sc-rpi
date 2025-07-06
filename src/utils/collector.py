"""Contains the `Collector` class."""

from __future__ import annotations

from ast import literal_eval

from models.responses import Client


class Collector:
    """Used to collect information of clients of SC RPI."""

    def __init__(self) -> None:
        """Initialize the instance (constructor)."""
        self._clients: set[tuple[str, int]] = set()

    def add_client(self, client: tuple[str, int]) -> None:
      """Add a client.

      Args:
          client (str): The result of the
            `request.get_extra_info("peername", request.remote)` method of the `Request`
            class (`aiohttp` library).

      """
      self._clients.add(client)

    def remove_client(self, client: tuple[str, int]) -> None:
      """Remove a client.

      Args:
          client (str): The result of the
            `request.get_extra_info("peername", request.remote)` method of the `Request`
            class (`aiohttp` library).

      """
      self._clients.remove(client)

    def get_clients(self) -> list[Client]:
      """Get all clients.

      Returns:
          list[Client]: List of clients.

      """
      return [Client(client[0], int(client[1])) for client in self._clients]
