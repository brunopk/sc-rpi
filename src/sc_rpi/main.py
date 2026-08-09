"""Starts the application."""

from __future__ import annotations

import logging

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

from sc_rpi.paho import callbacks
from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.logging import configure_logging
from sc_rpi.worker import Worker

# TODO: implement connection verification as before (sending ping to the default gateway)
# TODO: generate folder structure diagram with Claude

_LOGGER = logging.getLogger(__name__)

config = load_configurations()
configure_logging(config)

if config.env == "dev":
    _LOGGER.info("Starting application (press CTRL+C to exit)")
else:
    _LOGGER.info("Starting application")

client = Client(CallbackAPIVersion.VERSION2)
worker = Worker(config, client)

client.on_message = callbacks.on_message
client.on_connect = callbacks.on_connect
client.user_data_set((config, worker))
client.username_pw_set(
    config.mqtt.broker_config.username,
    config.mqtt.broker_config.password,
)

_LOGGER.info("Connecting to MQTT broker on %s", config.mqtt.broker_config.host)
client.connect(config.mqtt.broker_config.host, config.mqtt.broker_config.port,60)

worker.start()

try:
    client.loop_forever()
except Exception as ex:
    _LOGGER.exception("Error", exc_info=ex)
finally:
    _LOGGER.info("Disconnecting from the MQTT broker")
    client.disconnect()
