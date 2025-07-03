"""Test that all commands executes correctly.

This tests also validates that each command validates its own arguments.
"""

import logging
from configparser import ConfigParser
from json import dumps
from unittest import TestCase
from dataclasses import asdict

from command_parser import CommandParser
from controllers import HardwareController
from models.responses import Response, ResponseOk
from models.responses import Section


class TestCommandExecution(TestCase):
    """Test that all commands executes correctly.

    This tests also validates that each command validates its own arguments.
    """

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        config = ConfigParser()
        config.read("./config.ini")
        logging.basicConfig(level=None)
        hw_controller = HardwareController(config)
        self.parser = CommandParser(hw_controller)

    def test_disconnect(self) -> None:
        """Test case test_disconnect."""
        command_name = "disconnect"

        cmd = self.parser.parse(f'{{"name": "{command_name}"}}')
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

    def test_section_add(self) -> None:
        """Test case test_section_add."""
        command_name = "section_add"

        cmd = self.parser.parse(
            f'{{"name": "{command_name}", "args": {{"sections": []}}}}',
        )
        cmd.validate_arguments()
        resp = cmd.run()

        self.assertIsInstance(resp, Response)

    def test_section_edit(self) -> None:
        """Test case test_section_edit."""
        command_name = "section_edit"

        section_add_cmd_dict = {
            "name": "section_add",
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

    def test_section_remove(self) -> None:
        """Test case test_section_remove."""
        command_name = "section_remove"

        cmd = self.parser.parse(
            f'{{"name": "{command_name}", "args": {{"sections": []}}}}',
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


