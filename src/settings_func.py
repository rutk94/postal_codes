import os
from typing import Optional


def get_integer_or_none(
    variable_name: str, default: Optional[int] = None
) -> Optional[int]:
    value_str: str = str(os.getenv(variable_name, default=default)).replace('_', '')
    value: Optional[int] = int(value_str) if value_str.isdigit() else None
    return value
