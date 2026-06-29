"""Contains the `Worker` class."""

from __future__ import annotations

import logging
from http import HTTPStatus
from json import loads
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING

from sc_rpi.commands.base import Command
from sc_rpi.controllers import HardwareController
from sc_rpi.enums.error_code import ErrorCode
from sc_rpi.enums.homeassistant import ColorMode, Schema, State
from sc_rpi.errors.api_error import ApiError
from sc_rpi.models import Color
from sc_rpi.models.homeassistant import HACommand, HAMQTTDiscoveryMessage, HAState
from sc_rpi.utils.commands.mappings import map_ha_command_to_sc_rpi_command
from sc_rpi.utils.mappings import map_exception
from sc_rpi.utils.topic_utils import (
    SC_RPI_RESULT_TOPIC,
    build_ha_command_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
    matches_ha_command_topic,
    matches_sc_rpi_command_topic,
)

# TODO: check why the applications seems to hang up after catching an exception when receiving a command (try sending two commands one after the other)
# TODO: state (on/off) should be published when starting the application (test that state is correctly synchronized)
# TODO: test forcing an error , verify this error is not raised: mashumaro.exceptions.UnresolvedTypeReferenceError: Class Error has unresolved type reference ErrorCode in some of its fields
# TODO: detect where the command comes from (HA or user) and send result only for the corresponding topics (add this into a Gist)

if TYPE_CHECKING:
    from paho.mqtt.client import Client, MQTTMessage

    from sc_rpi.config import Config
    from sc_rpi.models import SectionInternalRepresentation

_LOGGER = logging.getLogger(__name__)


def _parse_ha_cmd(cmd: str) -> HACommand:
    """Parse a message from Home Assistant.

    Args:
        cmd (str): Command from Home Assistant (UTF-8 decoded).

    Raises:
        ApiError: Raises this error if there's any problem parsing the message, \
            for example if some attribute don't have required format.

    Returns:
        HACommand:

    """
    try:
        cmd_as_dict: dict = loads(cmd)
        return HACommand.from_dict(cmd_as_dict)
    except Exception as ex:
        raise ApiError(
            HTTPStatus.BAD_REQUEST,
            ErrorCode.BAD_REQUEST,
            "Invalid JSON",
        ) from ex

def _parse_sc_rpi_cmd(
    cmd: str,
    config: Config,
    hw_controller: HardwareController,
) -> Command:
    """Parse a message from the user to SC RPi (command).

    Args:
        cmd (str): Command for SC RPi decoded (UTF-8).
        config (Config): SC RPi configuration.
        hw_controller (HardwareController): Used to interact with the hardware.


    Raises:
        ApiError: Raises this error if there's any problem parsing the message, for \
         example if some attribute don't have required format.

    Returns:
        Command:

    """
    try:
        cmd_as_dict: dict = loads(cmd)
        return Command.from_dict_wrapper(cmd_as_dict, config, hw_controller)
    except Exception as ex:
        raise ApiError(
            HTTPStatus.BAD_REQUEST,
            ErrorCode.BAD_REQUEST,
            "Invalid JSON",
        ) from ex

class Worker(Thread):
    """Collects messages and process them.

    Messages are collected from an internal queue (see `put_message` method) and process
    the in a dedicated thread. Current implementation uses **one** thread to process all
    messages.
    """

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize the instance (constructor).

        Args:
          config (Config): SC RPi configuration.
          client (Client): Paho MQTT client.

        """
        super().__init__(daemon=True, name="WorkerThread")

        _LOGGER.info("Initializing worker")

        self._config = config
        self._client = client
        self._hw_controller = HardwareController(config)
        self._message_queue: Queue[MQTTMessage] = Queue()

    def put_message(self, message: MQTTMessage) -> None:
        """Put a message into a internal queue to be processed.

        Args:
          message (MQTTMessage): Message to be processed.

        """
        self._message_queue.put(message)

    def run(self) -> None:
        """Code to be executed in the new thread."""
        self._publish_ha_entities(self._hw_controller.list_sections())

        while True:
            msg = self._message_queue.get()
            msg_decoded = msg.payload.decode()

            _LOGGER.debug("Message received on topic %s: %s", msg.topic, msg_decoded)

            """
            All commands, from Home Assistant or from user, are first converted to \
                an SC RPi command
            """

            try:
                sc_rpi_command = None

                if matches_ha_command_topic(msg.topic):
                    ha_command = _parse_ha_cmd(msg_decoded)
                    sc_rpi_command = map_ha_command_to_sc_rpi_command(
                        ha_command,
                        msg.topic,
                        self._config,
                        self._hw_controller,
                    )
                elif matches_sc_rpi_command_topic(msg.topic):
                    sc_rpi_command = _parse_sc_rpi_cmd(
                        msg_decoded,
                        self._config,
                        self._hw_controller,
                    )
                else:
                    _LOGGER.warning(
                        "Message received on unexpected topic %s", msg.topic
                    )
                    continue

                if sc_rpi_command is not None:
                    sc_rpi_command.validate()

                    command_result = sc_rpi_command.run()

                    if len(command_result.keys()) == 0:
                        _LOGGER.warning(
                            "No topics to return result of %s command",
                            sc_rpi_command.command_name,
                        )
                    else:
                        for topic_name in command_result:
                            topic_payload = (
                                command_result[topic_name]
                                if isinstance(command_result[topic_name], str)
                                else command_result[topic_name].to_json()
                            )
                            _LOGGER.debug("Publishing result to %s topic", topic_name)
                            self._client.publish(topic_name, topic_payload)

            except Exception as ex:
                self._handle_exception(sc_rpi_command, ex)

            self._message_queue.task_done()

    def _publish_ha_entities(
        self, sections: list[SectionInternalRepresentation]
    ) -> None:
        for section in sections:
            command_topic = build_ha_command_topic(section.id)
            state_topic = build_ha_state_topic(section.id)
            discovery_topic = build_ha_discovery_topic(section.id)

            """
            HA requires unique_id it to be unique to allow the entity to be managed
            through the UI
            """

            _LOGGER.info(
                "Sending discovery message for section %s (start=%d, end=%d)",
                section.id,
                section.start,
                section.end,
            )
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
            # TODO: add retain=True (this is just for testing)
            self._client.publish(discovery_topic, discovery_message.to_json())

            # TODO: line 232 and 237 should be in a helper function
            _LOGGER.info("Sending state for section %s", section.id)
            section_color = Color(
                section.color_list[0][0],
                section.color_list[0][1],
                section.color_list[0][2],
            )
            state = HAState(
                State.ON if section.is_on else State.OFF, color=section_color
            )
            self._client.publish(state_topic, state.to_json())

    def _handle_exception(
        self,
        sc_rpi_command: Command | None,
        ex: ApiError | Exception,
    ) -> None:
        """Handle the exception sending the corresponding message through the \

        corresponding topics.

        Args:
            sc_rpi_command (Command): Use this parameter if the exception was caused \
                by a command.
            ex (ApiError | Exception): Exception to be handled.

        """
        msg = (
            f"Error executing command {sc_rpi_command.command_name}"
            if sc_rpi_command is not None
            else "Error executing command"
        )
        if isinstance(ex, ApiError):
            _LOGGER.warning(msg, exc_info=ex)
        else:
            _LOGGER.exception(msg, exc_info=ex)

        try:
            sc_rpi_result = map_exception(ex, sc_rpi_command)
            self._client.publish(SC_RPI_RESULT_TOPIC, sc_rpi_result.to_json())
        except Exception as ex:
            _LOGGER.warning("Error sending result", exc_info=ex)
