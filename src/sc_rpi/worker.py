"""Contains the `Worker` class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from json import loads
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING

from sc_rpi.controllers import HardwareController
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.enums.homeassistant.color_mode import ColorMode
from sc_rpi.enums.homeassistant.schema import Schema
from sc_rpi.errors import ApiError
from sc_rpi.models.homeassistant import HACommand, HAMQTTDiscoveryMessage
from sc_rpi.utils.commands.mappings import map_ha_command_to_sc_rpi_command
from sc_rpi.utils.topic_utils import (
    build_ha_command_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
    matches_ha_command_topic,
    matches_sc_rpi_command_topic,
)

# TODO: check why the applications seems to hang up after catching an exception when receiving a command (try sending two commands one after the other)

if TYPE_CHECKING:
    from paho.mqtt.client import Client, MQTTMessage

    from sc_rpi.models.command import Command
    from sc_rpi.models.config import Config
    from sc_rpi.models.config.strip_config import Section

# TODO: rename all logger to LOGGER
LOGGER = logging.getLogger(__name__)

class Worker(Thread):
    """Collects messages and process them.

    Collects messages in a internal queue (see `put_message` method) and process \
        them in a dedicated thread. Current implementation uses **one** thread to \
            process all messages.
    """

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize the instance (constructor).

        Args:
          config (Config): SC RPi configuration.
          client (Client): Paho MQTT client.

        """
        super().__init__(daemon=True, name="WorkerThread")

        LOGGER.debug("Initializing worker")

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
            msg_payload = msg.payload.decode()

            LOGGER.debug("Message received on topic %s: %s", msg.topic, msg_payload)

            """
            All commands (from Home Assistant or from user) are first converted to \
                an SC RPi command
            """

            try:
                sc_rpi_command = None

                if matches_ha_command_topic(msg.topic):
                    ha_command = self._parse_ha_msg(msg_payload)
                    command = map_ha_command_to_sc_rpi_command(
                        ha_command,
                        msg.topic,
                        self._config,
                        self._hw_controller,
                    )
                elif matches_sc_rpi_command_topic(msg.topic):
                    # TODO: CONTINUE with _parse_sc_rpi_msg
                    sc_rpi_command = self._parse_sc_rpi_msg(msg)
                else:
                    LOGGER.warning("Message received on unexpected topic %s", msg.topic)
                    continue

                if sc_rpi_command is not None:
                    command.validate()

                    command_result = sc_rpi_command.run()

                    if len(command_result.keys()) == 0:
                        LOGGER.warning(
                            "No topics to return result of %s command",
                            sc_rpi_command.name,
                        )
                    else:
                        for topic_name in command_result:
                            topic_payload = (
                                command_result[topic_name]
                                if isinstance(command_result[topic_name], str)
                                else command_result[topic_name].to_json()
                            )
                            LOGGER.debug("Publishing result to %s topic", topic_name)
                            self._client.publish(topic_name, topic_payload)
                            # TODO: CONTINUE send sc_rpi error in the corresponding topic

            except ApiError as ex:
                if sc_rpi_command is not None:
                    LOGGER.warning(
                        "Error executing command %s",
                        sc_rpi_command.name,
                        exc_info=ex,
                    )
                else:
                    LOGGER.warning("Error executing command", exc_info=ex)

            except Exception as ex:
                if sc_rpi_command is not None:
                    LOGGER.exception(
                        "Error executing command %s",
                        sc_rpi_command.name,
                        exc_info=ex,
                    )
                else:
                    LOGGER.exception("Error executing command", exc_info=ex)

            self._message_queue.task_done()

    def _publish_ha_entities(self, sections: list[Section]) -> None:
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
                object_id=section.id,
                schema=Schema.JSON,
                state_topic=state_topic,
                supported_color_modes=[ColorMode.RGB],
                unique_id=section.id,
            )
            discovery_topic = build_ha_discovery_topic(section.id)
            # TODO: add retain=True (this is just for testing)
            self._client.publish(discovery_topic, discovery_message.to_json())

            LOGGER.info(
                "Strip section from %d to %d published to Home Assistant as %s",
                section.start,
                section.end,
                section.id,
            )

    def _parse_ha_msg(self, msg: str) -> HACommand:
        """Parse a message from Home Assistant (command topic).

        Args:
            msg (MQTTMessage): Message received in the `on_message` callback passed to \
                the Paho client object.

        Raises:
            ApiError: Raises this error if there's any problem parsing the message, \
                for example if some attribute don't have required format.

        Returns:
            HACommand:

        """
        try:
            cmd_as_dict: dict = loads(msg)
            return HACommand.from_dict(cmd_as_dict)
        except Exception as ex:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                ErrorCode.BAD_REQUEST,
                "Invalid JSON",
            ) from ex

    def _parse_sc_rpi_msg(self, msg: MQTTMessage) -> Command:
        # TODO: implement similar to _parse_ha_msg method
        LOGGER.info("_process_sc_rpi_command")

        try:
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
