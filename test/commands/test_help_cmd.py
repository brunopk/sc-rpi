"""Contains the `TestHelp` class."""

from unittest import TestCase

from sc_rpi.commands.help import HelpCmd
from sc_rpi.models import Response
from sc_rpi.models.command import Command


class TestHelp(TestCase):
    """Tests for `help` command."""

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        command =Command.from_dict({"name": "help"})
        command.validate()
        resp = command.run()

        self.assertIsInstance(resp, Response)
        self.assertIsInstance(resp.to_json(), str)
        self.assertEqual(resp.command_name, HelpCmd.name)

