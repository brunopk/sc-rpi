from typing import Optional
from dataclasses import dataclass
from http import HTTPStatus

@dataclass
class Response:

    status: HTTPStatus = HTTPStatus.ACCEPTED

    description: Optional[str] = None

    data: Optional[dict] = None

    def __init__(self, status: HTTPStatus, description: Optional[str] = None, data: Optional[dict] = None):
        self.status = status
        self.description = description if description is not None else " ".join(status.name.lower().split("_"))
        self.data = data


class Error(Response):

    def __init__(self, status: HTTPStatus, description: Optional[str] = None):
        super().__init__(status=status, description=" ".join(status.name.lower().split("_")) if description is None else description)
