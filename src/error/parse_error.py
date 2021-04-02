from typing import List, Union
from jsonschema import ValidationError


def get_path(e: ValidationError) -> str:
    result = 'args'
    for e in e.absolute_path:
        if isinstance(e, int):
            result += f'[{e}]'
        else:
            result += f'.{e}'
    return result


class ParseError(Exception):

    def __init__(self, errors: List[Union[ValidationError, str]]):
        aux1 = [f'error in {get_path(e)} : {e.message}' for e in errors if isinstance(e, ValidationError)]
        aux2 = [e for e in errors if isinstance(e, str)]
        self.errors = aux1 if len(aux1) > 0 else aux2
