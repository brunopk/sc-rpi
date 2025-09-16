"""Contains the `Worker` class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from json import loads
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING

from sc_rpi.controllers import HardwareController
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.homeassistant import HAMQTTDiscoveryMessage
from sc_rpi.utils.mqtt import (
    build_ha_command_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
    matches_ha_command_topic,
    matches_sc_rpi_command_topic,
)

if TYPE_CHECKING:
    from paho.mqtt.client import Client, MQTTMessage

    from sc_rpi.models.command import Command
    from sc_rpi.models.config import Config
    from sc_rpi.models.config.strip_config import Section

logger = logging.getLogger(__name__)

class Worker(Thread):
    """Process messages in a dedicated thread (worker thread)."""

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize the instance (constructor).

        Args:
          config (Config): SC RPi configuration.
          client (Client): Paho MQTT client.

        """
        super().__init__(daemon=True, name="WorkerThread")
        logger.debug("Initializing worker")
        self._config = config
        self._client = client
        self._hw_controller = HardwareController(config)
        self._message_queue : Queue[MQTTMessage] = Queue()

    def put_message(self, message: MQTTMessage) -> None:
        """Put a message into a internal queue to be processed.

        Args:
          message (MQTTMessage): Message to be processed.

        """
        self._message_queue.put(message)

    def run(self) -> None:
        """Code to be executed in the new thread."""
        self._publish_ha_entities(self._config.strip_config.sections)

        while True:
            msg = self._message_queue.get()

            logger.debug("Message received for %s topic", msg.topic)

            try:
                # TODO: CONTINUE
                if matches_ha_command_topic(msg.topic):
                    ha_command = self._get_ha_command(msg)
                if matches_sc_rpi_command_topic(msg.topic):
                    sc_rpi_command = self._get_sc_rpi_command(msg)

                sc_rpi_command.validate()
                sc_rpi_command.run()
            except ApiError as ex:
                logger.exception(
                    "Error executing %s command: %s",
                    sc_rpi_command.command_name,
                    ex.message,
                    exc_info=ex,
                )
                # TODO: continue
            except Exception as ex:
                logger.exception(
                    "Error executing %s command: %s",
                    sc_rpi_command.command_name,
                    exc_info=ex,
                )
                # TODO: continue

            self._message_queue.task_done()

    def _publish_ha_entities(self, sections: list[Section]) -> None:
        logger.info("Publishing entities for Home Assistant")
        for section in sections:
            command_topic = build_ha_command_topic(section.id)
            state_topic = build_ha_state_topic(section.id)

            """
            HA requires unique_id it to be unique to allow the entity to be managed \
                through the UI
            """

            discovery_message = HAMQTTDiscoveryMessage(
                section.name,
                brightness=True,
                command_topic=command_topic,
                rgb=True,
                schema="json",
                state_topic=state_topic,
                object_id=section.id,
                unique_id=section.id,
            )
            discovery_topic = build_ha_discovery_topic(section.id)
            # TODO: add retain=True (this is just for testing)
            logger.info(
                "Publishing strip section %s (%d - %d)",
                section.id,
                section.start,
                section.end,
            )
            self._client.publish(discovery_topic, discovery_message.to_json())


    def _get_ha_command(self, msg: MQTTMessage) -> None:
        logger.info("_process_ha_command")
        try:
            cmd_as_dict: dict = loads(msg.payload.decode())
            # cmd = from_dict(data_class=HACommand, data=cmd_as_dict)
            # print(cmd)
        except Exception as ex:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Invalid JSON",
            ) from ex
        if not isinstance(cmd_as_dict, dict):
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Invalid JSON",
            )

        # TODO: continue

    def _get_sc_rpi_command(self, msg: MQTTMessage) -> Command:
        logger.info("_process_sc_rpi_command")

        try:
            # TODO: Take into account that if some error occurs when parsing from `dict` (`from_dict` method), Mashumaro will raise `InvalidFieldValue`.
            cmd_as_dict: dict = loads(msg.payload.decode())
            cmd_name = cmd_as_dict.get("name")
            cmd_args = cmd_as_dict.get("args")
        except Exception as ex:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Invalid JSON",
            ) from ex

        if not isinstance(cmd_as_dict, dict):
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Invalid JSON",
            )

        if cmd_name is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "'name' not defined",
            )

        if cmd_args is None:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "'args' not defined",
            )

        cmd_class = self._command_dictionary.get(cmd_name)
        if cmd_class is None:
            raise ApiError(
                HTTPStatus.NOT_FOUND,
                ErrorCode.COMMAND_NOT_FOUND,
                f"Command {cmd_name} not found",
            )

        return cmd_class(
            cmd_args,
            config=self._config,
            hw_controller=self._hw_controller,
        )
