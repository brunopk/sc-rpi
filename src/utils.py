from re import match
from webcolors import hex_to_rgb
from typing import Tuple


def parse_color(c: str) -> Tuple[int, int, int]:
    """
    Parse and returns the corresponding color

    :param c: RGB or hexadecimal string representation of the color
    :return: the color
    :raises ValueError: if c is not correctly defined
    """
    try:
        c = hex_to_rgb(c)
        (red, green, blue) = c.red, c.green, c.blue
    except ValueError as e:
        regex_rgb = r"^rgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$"
        _match = match(regex_rgb, c)
        if _match is not None:
            red = int(_match.groups()[0])
            green = int(_match.groups()[1])
            blue = int(_match.groups()[2])
            if 0 > red or 0 > green or 0 > blue or 255 < red or 255 < green or 255 < blue:
                raise ValueError()
        else:
            raise ValueError()
    return red, green, blue


# noinspection PyShadowingBuiltins
def bool(b: str):
    """
    Parse a string as bool:

        - 'True', 'true', 'y' , '1' -> True
        - 'False', 'false', 'n', '0' -> False

    :raise ValueError: if string cannot be parsed as detailed above
    """
    if b in ['True', 'true', 'y' , '1']:
        return True
    elif b in ['False', 'false', 'n', '0']:
        return False
    else:
        raise ValueError()
