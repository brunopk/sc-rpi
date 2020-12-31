from json import dumps


class Response:

    def __init__(self, status, result: dict):
        self.status = status
        self.result = result

    def to_json(self) -> str:
        """
        Returns JSON stringified representation of the response.
        """
        json = {
            'status': self.status.value,
            'message': self.status.phrase,
            'result': self.result
        }
        return dumps(json)
