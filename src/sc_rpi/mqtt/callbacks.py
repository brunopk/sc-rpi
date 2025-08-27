"""Callback functions required by Paho library."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from paho.mqtt.client import MQTTMessage

from sc_rpi.utils.mqtt.topic_utils import (
    build_ha_command_topic,
    build_sc_rpi_command_topic,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from paho.mqtt.client import Client, MQTTMessage

    from sc_rpi.models.config import Config
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
    """Use this function as `on_connect` callback.

    Args:
        client (Client): MQTT client (created with the `paho`library)
        userdata (tuple[Config, Worker]): additional attributes provided to with \
            `user_data_set` method)
        _flags (_type_): _description_
        reason_code (_type_): _description_
        _properties (_type_): _description_

    """
    config = userdata[0]
    if reason_code.is_failure:
        error_msg = f"Failed to connect: {reason_code}. "
        "loop_forever() will retry connection"
        logger.error(error_msg)
    else:
        ha_command_topic = build_ha_command_topic(
            config.mqtt_config.topics_config.ha_topic_prefix,
        )
        logger.info("Subscribing to %s", ha_command_topic)
        client.subscribe(ha_command_topic)

        sc_rpi_command_topic = build_sc_rpi_command_topic(
            config.mqtt_config.topics_config.sc_rpi_topic_prefix,
        )
        logger.info("Subscribing to %s", sc_rpi_command_topic)
        client.subscribe(sc_rpi_command_topic)

