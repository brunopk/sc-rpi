from typing import Optional
from json import dumps
from http import HTTPStatus


class Response:

    def __init__(self, result: Optional[dict] = None, status: HTTPStatus = HTTPStatus.OK, description: Optional[str] = None):
        self.status = status
        self.message = status.name
        self.description = description
        self.result = result

    def to_json(self) -> str:
        """
        Returns JSON stringified representation of the response.
        """
        json = {
            'status': self.status.value,
            'message': self.status.phrase,
        }

        if self.result is not None:
            json['result'] = self.result
        if self.description is not None:
            json['description'] = self.description

        return dumps(json)


class Error(Response):

    def __init__(self, status: HTTPStatus, description: Optional[str] = None):
        super().__init__(status=status, description=description)
