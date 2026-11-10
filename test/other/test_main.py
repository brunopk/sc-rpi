"""Tests for the order of the MQTT calls made by `main.py`."""

import runpy
from unittest import TestCase
from unittest.mock import MagicMock, patch

from sc_rpi.utils.config import load_configurations


class TestMain(TestCase):
    """Tests for the startup and shutdown sequence."""

    def test_last_will_before_connect_and_offline_before_disconnect(self) -> None:
        """Set the LWT before `connect` and publish `offline` before `disconnect`."""
        client = MagicMock()
        client.loop_forever.return_value = None
        config = load_configurations("config_test.yaml")
        with (
            patch("paho.mqtt.client.Client", return_value=client),
            patch("sc_rpi.utils.config.load_configurations", return_value=config),
        ):
            runpy.run_module("sc_rpi.main")

        names = [c[0] for c in client.method_calls]
        self.assertLess(names.index("will_set"), names.index("connect"))
        will_args = client.will_set.call_args
        self.assertEqual(("scrpi/status", "offline"), will_args.args)
        self.assertTrue(will_args.kwargs["retain"])

        offline_index = next(
            i
            for i, c in enumerate(client.method_calls)
            if c[0] == "publish" and c[1][:2] == ("scrpi/status", "offline")
        )
        self.assertLess(offline_index, names.index("disconnect"))
