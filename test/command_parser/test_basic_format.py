"""Test basic format (JSON format requirements) for all commands.

This tests do not validate specific command arguments.
"""

import logging
from unittest import TestCase

from sc_rpi.controllers import HardwareController
from sc_rpi.utils.commands import CommandParser
from sc_rpi.utils.config.main import load_configurations


class TestCreatingSections(TestCase):
    """Test basic format (JSON format requirements) for all commands.

    This tests do not validate specific command arguments.
    """

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        config = load_configurations()
        logging.basicConfig(level=None)
        hw_controller = HardwareController(config)
        self.parser = CommandParser(config, hw_controller)

    def test_add_section_basic_format(self) -> None:
        """Test case test_add_section_basic_format."""
        self.parser.parse('{"name": "add_section"}')

    def test_edit_section_basic_format(self) -> None:
        """Test case test_edit_section_basic_format."""
        self.parser.parse('{"name": "edit_section"}')

    def test_get_config_basic_format(self) -> None:
        """Test case test_get_config_basic_format."""
        self.parser.parse('{"name": "get_config"}')

    def test_help_basic_format(self) -> None:
        """Test case test_help_basic_format."""
        self.parser.parse('{"name": "help"}')

    def test_remove_section_basic_format(self) -> None:
        """Test case test_remove_section_basic_format."""
        self.parser.parse('{"name": "remove_section"}')

    def test_reset_basic_format(self) -> None:
        """Test case test_reset_basic_format."""
        self.parser.parse('{"name": "reset"}')

    def test_status_basic_format(self) -> None:
        """Test case test_status_basic_format."""
        self.parser.parse('{"name": "status"}')

    def test_turn_on_basic_format(self) -> None:
        """Test case test_turn_on_basic_format."""
        self.parser.parse('{"name": "turn_on"}')

    def test_turn_off_basic_format(self) -> None:
        """Test case test_turn_off_basic_format."""
        self.parser.parse('{"name": "turn_off"}')

    def test_version_basic_format(self) -> None:
        """Test case test_version_basic_format."""
        self.parser.parse('{"name": "version"}')


