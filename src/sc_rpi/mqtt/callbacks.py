"""Callback functions required by Paho library."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from paho.mqtt.client import MQTTMessage

from sc_rpi.utils.mqtt import topic_utils

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from paho.mqtt.client import Client, MQTTMessage

    from sc_rpi.config import Config
    from sc_rpi.worker import Worker

def on_message(
    _client: Client,
    userdata: tuple[Config, Worker],
    msg: MQTTMessage,
) -> None:
    """Use this function as `on_message` callback."""
    worker = userdata[1]
    worker.put_message(msg)


def on_connect(
    client: Client,
    userdata: tuple[Config, Worker],
    _flags,
    reason_code,
    _properties,
) -> None:
    """Use this function as `on_connect` callback."""
    config = userdata[0]
    if reason_code.is_failure:
        error_msg = f"Failed to connect: {reason_code}. "
        "loop_forever() will retry connection"
        logger.error(error_msg)
    else:
        ha_command_topic = topic_utils.build_ha_command_topic(
            config.mqtt.topics.ha_topic_prefix,
        )
        logger.info("Subscribing to %s", ha_command_topic)
        client.subscribe(ha_command_topic)

        sc_rpi_command_topic = topic_utils.build_sc_rpi_command_topic(
            config.mqtt.topics.sc_rpi_topic_prefix,
        )
        logger.info("Subscribing to %s", sc_rpi_command_topic)
        client.subscribe(sc_rpi_command_topic)

