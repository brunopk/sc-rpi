from enums import ErrorCode
from typing import List, Union, Optional
from jsonschema import ValidationError


class ApiError(Exception):

    def __init__(
            self,
            code: ErrorCode,
            message: Optional[str] = None,
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.status = code.value
        self.message = \
            message if message is not None else self.__get_message__(code)

    def __get_message__(self, code):
        if code == ErrorCode.ALREADY_OFF:
            return "Already off"
        elif code == ErrorCode.ALREADY_ON:
            return "Already on"
        elif code == ErrorCode.EXECUTION_ERROR:
            return "Internal error executing this command"
        elif code == ErrorCode.OVERLAPPING:
            return "Section overlapping"
        else:
            return "No message"


class ParseError(ApiError):

    def __init__(self, errors: List[Union[str, ValidationError]]):
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
