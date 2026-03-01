"""Contains the `TestHelp` class."""

from unittest import TestCase

from sc_rpi.commands import Help
from sc_rpi.commands.base import Command


class TestHelp(TestCase):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command =Command.from_dict({"command_name": "help"})
        command.validate()
        command.run()
