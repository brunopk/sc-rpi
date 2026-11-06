"""Tests for `Worker` startup."""

import time
from unittest import TestCase
from unittest.mock import MagicMock

from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.topics import (
    build_ha_availability_topic,
    build_ha_discovery_topic,
    build_ha_state_topic,
)
from sc_rpi.worker import Worker


class TestWorkerStartup(TestCase):
    """Tests for what the worker publishes when it starts."""

    def test_startup_publishes_discovery_online_and_state(self) -> None:
        """Each boot section gets discovery, `online` and state, in that order."""
        config = load_configurations("config_test.yaml")
        client = MagicMock()
        worker = Worker(config, client)
        sections = worker._hw_controller.list_sections()  # noqa: SLF001

        worker.start()
        expected = len(sections) * 3
        for _ in range(100):
            if client.publish.call_count >= expected:
                break
            time.sleep(0.02)

        topics = [call.args[0] for call in client.publish.call_args_list]
        payloads = {call.args[0]: call.args[1] for call in client.publish.call_args_list}
        self.assertEqual(
            [build_ha_discovery_topic(s.id) for s in sections]
            + [build_ha_availability_topic(s.id) for s in sections]
            + [build_ha_state_topic(s.id) for s in sections],
            topics,
        )
        for section in sections:
            self.assertEqual("online", payloads[build_ha_availability_topic(section.id)])
            self.assertIn(
                build_ha_availability_topic(section.id),
                payloads[build_ha_discovery_topic(section.id)],
            )
