"""Test basic format (JSON format requirements) for all commands.

This tests do not validate specific command arguments.
"""

import logging
from unittest import TestCase

from controllers import HardwareController
from utils.commands import CommandParser
from utils.config import load_configurations


class TestCreatingSections(TestCase):
    """Test basic format (JSON format requirements) for all commands.

    This tests do not validate specific command arguments.
    """

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        config = load_configurations()
        logging.basicConfig(level=None)
        hw_controller = HardwareController(config)
        self.parser = CommandParser(hw_controller)

    def test_disconnect_basic_format(self) -> None:
        """Test case test_disconnect_basic_format."""
        self.parser.parse('{"name": "disconnect"}')

    def test_help_basic_format(self) -> None:
        """Test case test_help_basic_format."""
        self.parser.parse('{"name": "help"}')

    def test_reset_basic_format(self) -> None:
        """Test case test_reset_basic_format."""
        self.parser.parse('{"name": "reset"}')

    def test_section_add_basic_format(self) -> None:
        """Test case test_section_add_basic_format."""
        self.parser.parse('{"name": "section_add"}')

    def test_section_edit_basic_format(self) -> None:
        """Test case test_section_edit_basic_format."""
        self.parser.parse('{"name": "section_edit"}')

    def test_section_remove_basic_format(self) -> None:
        """Test case test_section_remove_basic_format."""
        self.parser.parse('{"name": "section_remove"}')

    def test_turn_on_basic_format(self) -> None:
        """Test case test_turn_on_basic_format."""
        self.parser.parse('{"name": "turn_on"}')

    def test_turn_off_basic_format(self) -> None:
        """Test case test_turn_off_basic_format."""
        self.parser.parse('{"name": "turn_off"}')

    def test_version_basic_format(self) -> None:
        """Test case test_version_basic_format."""
        self.parser.parse('{"name": "version"}')


