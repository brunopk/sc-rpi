"""Test that all commands executes correctly.

This tests also validates that each command validates its own arguments.
"""

import logging
from json import dumps
from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response, ResponseOk, Section
from sc_rpi.utils import Collector
from sc_rpi.utils.commands import CommandParser
from sc_rpi.utils.config.main import load_configurations

# TODO: test only commands (not parsing)

class TestCommandExecution(TestCase):
    """Test that all commands executes correctly.

    This tests also validates that each command validates its own arguments.
    """

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        config = load_configurations()
        logging.basicConfig(level=None)
        collector = Collector()
        hw_controller = HardwareController(config)
        self.parser = CommandParser(config, hw_controller, collector)

    def test_add_section(self) -> None:
        """Test case test_add_section."""
        command_name = "add_section"

        cmd = self.parser.parse(
            f'{{"name": "{command_name}", "args": {{"sections": []}}}}',
        )
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_disconnect(self) -> None:
        """Test case test_disconnect."""
        command_name = "disconnect"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_edit_section(self) -> None:
        """Test case test_edit_section."""
        command_name = "edit_section"

        section_add_cmd_dict = {
            "name": "add_section",
            "args": {
                "sections": [{
                    "start": 0,
                    "end": 10,
                    "color": "#ffff00",
                }],
            },
        }
        section_add_cmd_str = dumps(section_add_cmd_dict)
        section_add_cmd = self.parser.parse(section_add_cmd_str)

        resp = section_add_cmd.run()

        if (not isinstance(resp, ResponseOk)):
            raise Exception("resp must be a ResponseOk instance")
        if (resp.data is None):
            error_msg = '"data" cannot be None'
            raise KeyError(error_msg)
        sections = resp.data.get("sections")
        if (sections is None):
            error_msg = '"sections" cannot be None'
            raise KeyError(error_msg)
        first_section = sections[0]
        if (not isinstance(first_section, Section)):
            raise Exception("section[0] must be a Section instance")

        section_edit_cmd_dict = {
            "name": command_name,
            "args": {
                "section_id": first_section.id,
            },
        }
        section_edit_cmd_str = dumps(section_edit_cmd_dict)
        cmd = self.parser.parse(section_edit_cmd_str)
        cmd.validate_arguments()

        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_get_config(self) -> None:
        """Test case test_get_config."""
        command_name = "get_config"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_help(self) -> None:
        """Test case test_help."""
        command_name = "help"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_remove_section(self) -> None:
        """Test case test_remove_section."""
        command_name = "remove_section"

        cmd = self.parser.parse(
            f'{{"name": "{command_name}", "args": {{"sections": []}}}}',
        )
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_reset(self) -> None:
        """Test case test_reset."""
        command_name = "reset"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_status(self) -> None:
        """Test case test_status."""
        command_name = "status"

        cmd = self.parser.parse(
            f'{{"name": "{command_name}"}}',
        )
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_turn_on(self) -> None:
        """Test case test_turn_on.

        Only validates turning on all the strip.
        """
        command_name = "turn_on"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_turn_off(self) -> None:
        """Test case test_turn_on.

        Only validates turning on all the strip.
        """
        command_name = "turn_off"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_version(self) -> None:
        """Test case test_version."""
        command_name = "version"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)


