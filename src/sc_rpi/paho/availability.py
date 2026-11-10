"""Publish the global availability of SC RPi (`SC_RPI_AVAILABILITY_TOPIC`).

All messages are retained, so Home Assistant gets the current value even if it starts
after them.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sc_rpi.utils.homeassistant import AVAILABLE, UNAVAILABLE
from sc_rpi.utils.topics import SC_RPI_AVAILABILITY_TOPIC

if TYPE_CHECKING:
    from paho.mqtt.client import Client

_LOGGER = logging.getLogger(__name__)

_PUBLISH_TIMEOUT_SECONDS = 2


def publish_availability(
    client: Client, *, available: bool, wait: bool = False
) -> None:
    """Publish `online` or `offline` (retained) on the global availability topic.

    Use `available=True` after each successful connection (birth message). Use
    `available=False` with `wait=True` before a controlled disconnect: a clean
    disconnect makes the broker discard the last will, so `offline` has to be sent
    explicitly. Do not wait inside callbacks (it would block the network loop).

    A failure while waiting is logged and not raised, so the disconnect still happens.

    Args:
        client (Client): MQTT client.
        available (bool): `True` publishes `online`, `False` publishes `offline`.
        wait (bool): Wait until the message is published (up to a timeout).

    """
    payload = AVAILABLE if available else UNAVAILABLE
    info = client.publish(SC_RPI_AVAILABILITY_TOPIC, payload, retain=True)
    if wait:
        try:
            info.wait_for_publish(_PUBLISH_TIMEOUT_SECONDS)
        except (RuntimeError, ValueError):
            _LOGGER.exception("Could not publish %s", payload)


def set_last_will(client: Client) -> None:
    """Make the broker publish `offline` if the connection drops abruptly.

    Call it before `connect`.

    Args:
        client (Client): MQTT client.

    """
    client.will_set(SC_RPI_AVAILABILITY_TOPIC, UNAVAILABLE, retain=True)
