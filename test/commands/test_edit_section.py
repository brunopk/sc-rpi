"""Contains the `TestAddSection` class."""

import logging
from unittest import TestCase

from sc_rpi.commands.add_section import AddSection
from sc_rpi.commands.edit_section import EditSection
from sc_rpi.controllers import HardwareController
from sc_rpi.models.responses import Response, Section
from sc_rpi.utils.config import load_configurations


class TestEditSection(TestCase):
    """Tests for src/commands/edit_section.py."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set required configurations before running any test."""
        logging.basicConfig(level=None)
        cls.config = load_configurations()
        cls.hw_controller = HardwareController(config=cls.config)

    def setUp(self) -> None:
        """Set required configurations before running each test case."""
        self.hw_controller.remove_all_sections()

    def test_basic_invocation(self) -> None:
        """Test case test_basic_invocation."""
        section_add_cmd = AddSection(
            {
                "sections": [
                    {
                        "start": 0,
                        "end": 10,
                        "color": "#ffff00",
                    },
                ],
            },
            config=self.config,
            hw_controller=self.hw_controller,
        )
        resp = section_add_cmd.run()

        if (resp.payload is None):
            error_msg = '"payload" cannot be None'
            raise KeyError(error_msg)
        sections = resp.payload.sections
        if (sections is None):
            error_msg = '"sections" cannot be None'
            raise KeyError(error_msg)
        first_section = sections[0]
        if (not isinstance(first_section, Section)):
            raise Exception("section[0] must be a Section instance")

        section_edit_cmd = EditSection(
            {
                "section_id": first_section.id,
            },
            config=self.config,
            hw_controller=self.hw_controller,
        )
        section_edit_cmd.validate()
        resp = section_edit_cmd.run()

        self.assertIsInstance(resp, Response)

