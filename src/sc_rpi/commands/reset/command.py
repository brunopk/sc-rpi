"""Contains the `ResetCmd` class."""

from dataclasses import dataclass

from sc_rpi.commands.base import Command, CommandResult
from sc_rpi.enums.homeassistant import ColorMode, State
from sc_rpi.models.homeassistant import HAState
from sc_rpi.utils.commands.decorators import log_before_running
from sc_rpi.utils.commands.results import build_status_result
from sc_rpi.utils.mappings import map_color_to_ha_format
from sc_rpi.utils.topic_utils import SC_RPI_RESULT_TOPIC, build_ha_state_topic

# TODO: investigate a mechanism to rollback changes for example, in this command if something fails after invoking reset() but before render(), strip state should be rollbacked
# TODO: create a test for this

@dataclass
class Reset(Command[None]):
    """`reset` command."""

    command_name: str = "reset"

    def validate(self) -> None:
        """Validate the arguments.

        This method should be invoked before executing the command
        """

    @log_before_running()
    def run(self) -> CommandResult:
        """Execute the command.

        :return Response: Contains the result of the execution.
        """
        self._hw_controller.reset()

        result = {}
        sc_rpi_result_topic_value = build_status_result(
            self._hw_controller,
            self.command_name
        )
        result[SC_RPI_RESULT_TOPIC] = sc_rpi_result_topic_value

        for section in self._hw_controller.list_sections():
            ha_entity_state_topic = build_ha_state_topic(section.id)
            ha_entity_state = HAState(
                State.ON,
                brightness=self.command_args.brightness,
                color=map_color_to_ha_format(section.color_list[0]),
                color_mode=ColorMode.RGB,
            )
            result[ha_entity_state_topic] = ha_entity_state

        self._hw_controller.render()

        return result
