"""Contains the `TestAddSection` class."""

from unittest import TestCase

from sc_rpi.commands.help import HelpCmd
from sc_rpi.models.command import Command
from sc_rpi.models.responses import Response


class TestHelp(TestCase):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command =Command.from_dict({"name": "help"})
        command.validate()
        resp = command.run()
        self.assertIsInstance(resp, Response)

