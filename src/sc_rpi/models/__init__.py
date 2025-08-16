"""Contains models (`@dataclass` annotated classes)."""

from sc_rpi.models import command, homeassistant
from sc_rpi.models.error import Error
from sc_rpi.models.response import Response
from sc_rpi.models.section_aux import SectionAux
from sc_rpi.models.status_resp import StatusResp

__all__ = [
    "Error",
    "Response",
    "SectionAux",
    "StatusResp",
    "command",
    "homeassistant",
]
