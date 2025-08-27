"""Contains the `Worker` class."""

import logging
from http import HTTPStatus
from json import loads
from queue import Queue
from threading import Thread

from paho.mqtt.client import MQTTMessage

from sc_rpi.controllers import HardwareController
from sc_rpi.enums import ErrorCode
from sc_rpi.errors import ApiError
from sc_rpi.models.command import Command
from sc_rpi.models.config import Config
from sc_rpi.utils.mqtt import topic_utils

logger = logging.getLogger(__name__)

class Worker(Thread):
    """Process messages in a dedicated thread (worker thread)."""

    def __init__(self, config: Config) -> None:
        """Initialize the instance (constructor).

        Args:
          config (Config): SC RPi configuration.

        """
        super().__init__(daemon=True, name="WorkerThread")
        logger.debug("Initializing worker")
        self._message_queue : Queue[MQTTMessage] = Queue()
        self._config = config
        self._hw_controller = HardwareController(config)

    def put_message(self, message: MQTTMessage) -> None:
        """Put a message into a internal queue to be processed.

        Args:
          message (MQTTMessage): Message to be processed.

        """
        self._message_queue.put(message)

    def run(self) -> None:
        """Code to be executed in the new thread."""
        while True:
            msg = self._message_queue.get()

            logger.debug("Message received for %s topic", msg.topic)

            try:
                if topic_utils.matches_ha_command_topic(msg.topic):
                    ha_command = self._get_ha_command(msg)
                if topic_utils.matches_sc_rpi_command_topic(msg.topic):
                    sc_rpi_command = self._get_sc_rpi_command(msg)

                sc_rpi_command.validate()
                sc_rpi_command.run()
                #TODO: continue
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

    def _publish_ha_entities(self, ) -> None:
        logger.info("Publishing entities for Home Assistant")
        # TODO: CONTINUE load sections from yaml when application is starting

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
