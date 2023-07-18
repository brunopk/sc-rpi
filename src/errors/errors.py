from enums import ErrorCode
from typing import List, Union, Optional
from jsonschema import ValidationError
from http import HTTPStatus


class ApiError(Exception):

    def __init__(self, error_code: ErrorCode, message: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = error_code.value
        self.status = self._status(error_code)
        self.message = message if message is not None else self._message(error_code)

    def _message(self, error_code):
        if error_code == ErrorCode.ALREADY_OFF:
            return "already off"
        elif error_code == ErrorCode.ALREADY_ON:
            return "already on"
        elif error_code == ErrorCode.EXECUTION_ERROR:
            return "internal error executing this command"
        elif error_code == ErrorCode.OVERLAPPING:
            return "section overlapping"
        else:
            return "No message"

    def _status(self, error_code) -> HTTPStatus:
        if \
            error_code == ErrorCode.ALREADY_OFF \
            or error_code == ErrorCode.ALREADY_ON \
                or error_code == ErrorCode.OVERLAPPING:
            return HTTPStatus.CONFLICT
        elif \
            error_code == ErrorCode.BAD_REQUEST \
                or error_code == ErrorCode.PARSE_ERROR:
            return HTTPStatus.BAD_REQUEST
        else:
            return HTTPStatus.INTERNAL_SERVER_ERROR


class ParseError(ApiError):

    def __init__(self, errors: Union[List[ValidationError], List[str]]):
        super().__init__(ErrorCode.PARSE_ERROR)
        aux1 = [
            f'error in {self.__get_path__(e)} : {e.message}'
            for e in errors
            if isinstance(e, ValidationError)
        ]
        aux2 = [e for e in errors if isinstance(e, str)]
        self.message = str(aux1) if len(aux1) > 0 else str(aux2)

    def __get_path__(self, error: ValidationError):
        result = 'args'
        for e in error.absolute_path:
            if isinstance(e, int):
                result += f'[{e}]'
            else:
                result += f'.{e}'
        return result
