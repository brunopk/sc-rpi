"""Starts the application."""

from __future__ import annotations

import logging
from queue import Queue
from threading import Thread
from typing import Any

from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion

from sc_rpi.utils.config.main import configure_logging, load_configurations

# TODO: TEST all commands (turn_off DONE, turn_on DONE, status PENDING)
# TODO: uncomment all classes from rpi_ws281x used in src/controller.py
# TODO: fix disconnect

logger = logging.getLogger(__name__)

worker_queue: Queue[tuple[str, str]] = Queue()

config = load_configurations()
configure_logging(config)

def on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
    """Use this function as `on_message` callback."""
    worker_queue.put((msg.topic, msg.payload.decode()))

def on_connect(client: Client, userdata: Any, flags, reason_code, properties) -> None:
    """Use this function as `on_connect` callback."""
    if reason_code.is_failure:
        error_msg = f"Failed to connect: {reason_code}. "
        "loop_forever() will retry connection"
        logger.error(error_msg)
    else:
        homeassistant_subscription = f"{config.mqtt_config.homeassistant_topic}/#"
        logger.info("Subscribing to %s", homeassistant_subscription)
        client.subscribe(homeassistant_subscription)

def worker() -> None:
    """Process all messages from subscribed MQTT topics. \

    It should be run in a different thread.
    """
    while True:
        item = worker_queue.get()
        logger.info("Message topic : %s", item[0])
        logger.info("Message payload : %s", item[1])
        worker_queue.task_done()

if config.env == "dev":
    logger.info("Starting application (press CTRL+C to exit)")
else:
    logger.info("Starting application")

client = Client(CallbackAPIVersion.VERSION2)
worker_thread = Thread(target=worker, daemon=True, name="WorkerThread")

worker_thread.start()

client.on_message = on_message
client.on_connect = on_connect

logger.info("Connecting to MQTT broker on %s", config.mqtt_config.host)

client.username_pw_set(config.mqtt_config.username, config.mqtt_config.password)
client.connect(config.mqtt_config.host, config.mqtt_config.port, 60)

try:
    client.loop_forever()
except Exception as ex:
    logger.exception("Error", exc_info=ex)
finally:
    logger.info("Disconnecting from the MQTT broker")
    client.disconnect()
