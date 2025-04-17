import os
from typing import Optional


def get_integer_or_none(variable_name: str) -> Optional[int]:
    """
    Ensures that loaded environment variable is an integer if it exist.

    Args:
        variable_name (str): Name of environment variable

    Returns:
        value (Optional[int]): Loaded environment variable as integer or None
    """

    value: Optional[int] = None
    if os.getenv(variable_name):
        value = get_integer_or_die(variable_name)

    return value


def get_integer_or_die(variable_name: str, default: Optional[int] = None) -> int:
    """
    Ensures that loaded environment variable is an integer.
    Otherwise it raises an error.

    Args:
        variable_name (str): Name of environment variable
        default (Optional[int]): Default value of environment variable

    Returns:
        value (int): Integer type value of environment variable

    Raises:
        ValueError: If environment variable string is not numeric
            or default value type is not an integer
    """

    value_str: str = str(os.getenv(variable_name, default=default))

    if default and not isinstance(default, int):
        raise ValueError(
            f"Wrong value type. {default=} must be an integer if it's not None"
        )

    try:
        value: int = int(value_str)
    except ValueError:
        raise ValueError(f'Wrong value {variable_name=}. It must be a digit.')
    else:
        return value


def get_float_or_die(variable_name: str, default: Optional[float] = None) -> float:
    """
    Ensures that loaded environment variable is a float.
    Otherwise it raises an error.

    Args:
        variable_name (str): Name of environment variable
        default (Optional[float]): Default value of environment variable

    Returns:
        value (float): Integer type value of environment variable

    Raises:
        ValueError: If environment variable string is not numeric
            or default value type is not a float
    """

    value_str: str = str(os.getenv(variable_name, default=default))

    if default and not isinstance(default, float):
        raise ValueError(
            f"Wrong value type. {default=} must be a float if it's not None"
        )

    try:
        value: float = float(value_str)
    except ValueError:
        raise ValueError(f'Wrong value {variable_name=}. It must be a numeric.')
    else:
        return value
