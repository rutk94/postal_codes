import os
from typing import Optional


def get_integer_or_none(
    variable_name: str, default: Optional[int] = None
) -> Optional[int]:
    value_str: str = str(os.getenv(variable_name, default=default))
    try:
        value: Optional[int] = int(value_str)
    except ValueError:
        value = None

    return value


def get_float_or_none(
    variable_name: str, default: Optional[float] = None
) -> Optional[float]:
    value_str: str = str(os.getenv(variable_name, default=default))
    try:
        value: Optional[float] = float(value_str)
    except ValueError:
        value = None

    return value
