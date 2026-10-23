"""Utility functions to work with colors."""

MAX_RGB = 255

def is_valid_color(color: tuple[int, int, int]) -> bool:
    """Validate a color.

    Args:
        color (str): Color in hex notation.

    Returns:
        bool: Returns `True` if it's a valid color. Otherwise, returns `False`

    """
    return (
        0 <= color[0] <= MAX_RGB
        and 0 <= color[1] <= MAX_RGB
        and 0 <= color[2] <= MAX_RGB
    )

