"""Starts the application."""

from __future__ import annotations

import logging

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

from sc_rpi.mqtt import callbacks
from sc_rpi.utils.config import configure_logging, load_configurations
from sc_rpi.worker import Worker

# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: implement connection verification as before (sending ping to the default gateway)

logger = logging.getLogger(__name__)

config = load_configurations()
configure_logging(config)

if config.env == "dev":
    logger.info("Starting application (press CTRL+C to exit)")
else:
    logger.info("Starting application")

client = Client(CallbackAPIVersion.VERSION2)
worker = Worker(config, client)

client.on_message = callbacks.on_message
client.on_connect = callbacks.on_connect
client.user_data_set((config, worker))
client.username_pw_set(
    config.mqtt_config.broker_config.username,
    config.mqtt_config.broker_config.password,
)


logger.info("Connecting to MQTT broker on %s", config.mqtt_config.broker_config.host)
client.connect(
    config.mqtt_config.broker_config.host,
    config.mqtt_config.broker_config.port,
    60,
)

worker.start()

try:
    client.loop_forever()
except Exception as ex:
    logger.exception("Error", exc_info=ex)
finally:
    logger.info("Disconnecting from the MQTT broker")
    client.disconnect()
