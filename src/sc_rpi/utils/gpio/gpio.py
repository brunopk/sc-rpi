"""Contains functions to work with GPIO ports."""

from __future__ import annotations

import RPi.GPIO as GPIO


def turn_led_on(pin_number: int) -> None:
    """Turn a GPIO port on (HIGH)."""
    GPIO.output(pin_number, GPIO.HIGH)

def turn_led_off(pin_number: int) -> None:
    """Turn a GPIO port off (LOW)."""
    GPIO.output(pin_number, GPIO.LOW)

def cleanup_gpio_ports() -> None:
    """Clean all GPIO ports."""
    GPIO.cleanup()
