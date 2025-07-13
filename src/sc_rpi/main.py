"""Starts the application."""

from __future__ import annotations

import logging

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

from sc_rpi.mqtt import callbacks
from sc_rpi.utils.config import configure_logging, load_configurations
from sc_rpi.worker import Worker

# TODO: modify turn_on turn_off to turn on/off only sections (not the whole strip)
# TODO: TEST all commands (turn_off DONE, turn_on DONE, test that they turn off/turn on only specified sections)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: implement initializing strip from a JSON file with commands.

logger = logging.getLogger(__name__)

config = load_configurations()
configure_logging(config)

if config.env == "dev":
    logger.info("Starting application (press CTRL+C to exit)")
else:
    logger.info("Starting application")

worker = Worker(config)
worker.start()

client = Client(CallbackAPIVersion.VERSION2)
client.on_message = callbacks.on_message
client.on_connect = callbacks.on_connect
client.user_data_set((config, worker))
client.username_pw_set(
    config.mqtt.broker.username,
    config.mqtt.broker.password,
)
logger.info("Connecting to MQTT broker on %s", config.mqtt.broker.host)
client.connect(config.mqtt.broker.host, config.mqtt.broker.port, 60)

try:
    client.loop_forever()
except Exception as ex:
    logger.exception("Error", exc_info=ex)
finally:
    logger.info("Disconnecting from the MQTT broker")
    client.disconnect()
