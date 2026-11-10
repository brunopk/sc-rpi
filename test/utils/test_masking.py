"""Tests for `mask_secrets`."""

import json
from copy import deepcopy
from unittest import TestCase

from sc_rpi.utils.config import load_configurations
from sc_rpi.utils.config.masking import (
    SECRET_PATHS,
    SECRET_PLACEHOLDER,
    mask_secrets,
)


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

    def test_every_secret_path_is_masked(self) -> None:
        """No value stored at a secret path appears in the masked config."""
        config = load_configurations("config_test.yaml")
        for index, path in enumerate(SECRET_PATHS):
            secret = f"distinctive-secret-{index}"
            target = config
            for name in path[:-1]:
                target = getattr(target, name)
            setattr(target, path[-1], secret)

        masked = mask_secrets(deepcopy(config))

        self.assertGreater(len(SECRET_PATHS), 0)
        output = json.dumps(masked.to_dict())
        for index in range(len(SECRET_PATHS)):
            self.assertNotIn(f"distinctive-secret-{index}", output)
        self.assertIn(SECRET_PLACEHOLDER, output)

    def test_original_is_not_modified(self) -> None:
        """The given config keeps its real password."""
        config = load_configurations("config_test.yaml")
        original_password = config.mqtt.broker.password
        mask_secrets(config)
        self.assertEqual(original_password, config.mqtt.broker.password)
        self.assertNotEqual(SECRET_PLACEHOLDER, original_password)
