"""Models for MQTT Home Assistant messages."""

from sc_rpi.models.homeassistant.ha_command import HACommand
from sc_rpi.models.homeassistant.ha_mqtt_discovery_message import HAMQTTDiscoveryMessage

__all__ = ["HACommand", "HAMQTTDiscoveryMessage"]
