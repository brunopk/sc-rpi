"""Publish the global availability of SC RPi (`SC_RPI_STATUS_TOPIC`).

All messages are retained, so Home Assistant gets the current value even if it starts
after them.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sc_rpi.utils.homeassistant import AVAILABLE, UNAVAILABLE
from sc_rpi.utils.topics import SC_RPI_STATUS_TOPIC

if TYPE_CHECKING:
    from paho.mqtt.client import Client

_LOGGER = logging.getLogger(__name__)

_PUBLISH_TIMEOUT_SECONDS = 2


def publish_offline(client: Client) -> None:
    """Publish `offline`, and wait for it, before a controlled disconnect.

    A clean disconnect makes the broker discard the last will, so it has to be sent
    explicitly. A failure is logged and not raised, so the disconnect still happens.

    Args:
        client (Client): MQTT client.

    """
    try:
        client.publish(SC_RPI_STATUS_TOPIC, UNAVAILABLE, retain=True).wait_for_publish(
            _PUBLISH_TIMEOUT_SECONDS
        )
    except (RuntimeError, ValueError):
        _LOGGER.exception("Could not publish %s", UNAVAILABLE)


def publish_online(client: Client) -> None:
    """Publish `online` (birth message). Call it after each successful connection.

    Args:
        client (Client): MQTT client.

    """
    client.publish(SC_RPI_STATUS_TOPIC, AVAILABLE, retain=True)


def set_last_will(client: Client) -> None:
    """Make the broker publish `offline` if the connection drops abruptly.

    Call it before `connect`.

    Args:
        client (Client): MQTT client.

    """
    client.will_set(SC_RPI_STATUS_TOPIC, UNAVAILABLE, retain=True)
