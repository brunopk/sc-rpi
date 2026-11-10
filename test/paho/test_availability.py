"""Tests for the global availability messages and the `on_connect` birth message."""

from unittest import TestCase
from unittest.mock import MagicMock, call

from sc_rpi.paho.availability import publish_offline, publish_online, set_last_will
from sc_rpi.paho.callbacks import on_connect


class TestAvailability(TestCase):
    """Tests for the LWT, birth and shutdown messages."""

    def test_on_connect_failure_publishes_nothing(self) -> None:
        """A failed connection publishes and subscribes to nothing."""
        client = MagicMock()
        on_connect(client, (None, None), None, self._reason_code(failure=True), None)
        client.publish.assert_not_called()
        client.subscribe.assert_not_called()

    def test_on_connect_publishes_online_before_subscribing(self) -> None:
        """The birth message is retained and sent before the subscriptions."""
        client = MagicMock()
        on_connect(client, (None, None), None, self._reason_code(failure=False), None)
        names = [c[0] for c in client.method_calls]
        self.assertEqual("publish", names[0])
        self.assertIn("subscribe", names)
        self.assertEqual(
            call.publish("scrpi/status", "online", retain=True), client.method_calls[0]
        )

    def test_publish_offline_waits_for_publication(self) -> None:
        """The shutdown message is retained and awaited."""
        client = MagicMock()
        publish_offline(client)
        client.publish.assert_called_once_with("scrpi/status", "offline", retain=True)
        client.publish.return_value.wait_for_publish.assert_called_once()

    def test_publish_offline_does_not_raise(self) -> None:
        """A failed publication is logged, so the disconnect still happens."""
        client = MagicMock()
        client.publish.return_value.wait_for_publish.side_effect = RuntimeError("x")
        with self.assertLogs("sc_rpi.paho.availability", level="ERROR"):
            publish_offline(client)

    def test_publish_online_is_retained(self) -> None:
        """The birth message is retained."""
        client = MagicMock()
        publish_online(client)
        client.publish.assert_called_once_with("scrpi/status", "online", retain=True)

    def test_set_last_will_is_retained_offline(self) -> None:
        """The LWT is `offline`, retained, on the global topic."""
        client = MagicMock()
        set_last_will(client)
        client.will_set.assert_called_once_with("scrpi/status", "offline", retain=True)

    def _reason_code(self, *, failure: bool) -> MagicMock:
        reason_code = MagicMock()
        reason_code.is_failure = failure
        return reason_code
