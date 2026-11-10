"""Tests for `mask_secrets`."""

from unittest import TestCase

from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.config.masking import SECRET_PLACEHOLDER, mask_secrets


class TestMaskSecrets(TestCase):
    """Tests for `mask_secrets`."""

    def test_password_is_masked_and_rest_unchanged(self) -> None:
        """Only the MQTT password changes."""
        config = load_configurations("config_test.yaml")

        masked = mask_secrets(config)

        self.assertEqual(SECRET_PLACEHOLDER, masked.mqtt.broker.password)
        self.assertEqual("test", masked.mqtt.broker.username)
        self.assertEqual(config.mqtt.broker.host, masked.mqtt.broker.host)
        self.assertEqual(config.mqtt.broker.port, masked.mqtt.broker.port)
        self.assertEqual(config.strip, masked.strip)
        self.assertEqual(config.description, masked.description)
        self.assertEqual(config.env, masked.env)

    def test_original_is_not_modified(self) -> None:
        """The given config keeps its real password."""
        config = load_configurations("config_test.yaml")
        original_password = config.mqtt.broker.password
        mask_secrets(config)
        self.assertEqual(original_password, config.mqtt.broker.password)
        self.assertNotEqual(SECRET_PLACEHOLDER, original_password)
