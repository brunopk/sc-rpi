"""Starts the application."""

from __future__ import annotations

import logging
import structlog

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

from sc_rpi.paho import callbacks
from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.logging import configure_logging
from sc_rpi.worker import Worker

# TODO: implement connection verification as before (sending ping to the default gateway)
# TODO: generate folder structure diagram with Claude
# TODO: CONTINUE use structlog.get_logger(__name__) Throughout the codebase (use formatted f-strings)

logger = structlog.get_logger(__name__)
client = Client(CallbackAPIVersion.VERSION2)

try:
    config = load_configurations()
    configure_logging(config)
    if config.env == "dev":
        logger.info("Starting application (press CTRL+C to exit)")
    else:
        logger.info("Starting application")

    worker = Worker(config, client)

    client.on_message = callbacks.on_message
    client.on_connect = callbacks.on_connect
    client.user_data_set((config, worker))
    client.username_pw_set(
        config.mqtt.broker_config.username,
        config.mqtt.broker_config.password,
    )

    logger.info(f"Connecting to MQTT broker on {config.mqtt.broker_config.host}")
    client.connect(config.mqtt.broker_config.host, config.mqtt.broker_config.port,60)

    worker.start()

    client.loop_forever()
except Exception:
    logger.exception("Error")
finally:
    logger.info("Disconnecting from the MQTT broker")
    client.disconnect()
