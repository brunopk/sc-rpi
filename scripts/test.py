from systemd.journal import JournalHandler
from typing import Optional
import RPi.GPIO as GPIO
import logging
from scapy.all import IP, ICMP, sr1


def configure_led_indicator(pin_number: int):
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(pin_number, GPIO.OUT)


def turn_led_indicator_on(pin_number: int):
  GPIO.output(pin_number, GPIO.HIGH)

def turn_led_indicator_off(pin_number: int):
  GPIO.output(pin_number, GPIO.LOW)

  

journal_handler = JournalHandler()
journal_handler.setFormatter(logging.Formatter('%(message)s'))
logging.basicConfig(handlers=[journal_handler])
logger = logging.getLogger(__name__)

led_indicator = 17
default_gateway = "192.168.0.1"
iface = "en0"
timeout=0.25

try:
  configure_led_indicator(led_indicator)
  reply = sr1(IP(dst=default_gateway)/ICMP(), iface=iface, timeout=timeout)
  if reply is None: 
     turn_led_indicator_off(led_indicator)
     logging.error(f"No answer from {default_gateway}")
     exit(1)
  turn_led_indicator_on(led_indicator)
except Exception as ex:
  turn_led_indicator_off(led_indicator)
  logging.exception(f"Error checking connection to {default_gateway}", exc_info=ex)
  exit(1)
finally:
  GPIO.cleanup()
