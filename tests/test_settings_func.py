import os
from pytest import mark
from typing import Optional

from src.settings_func import get_integer_or_none


@mark.parametrize('value, default', [('10', None), ('10_000', None), (None, 100)])
def test_get_integer_or_none_returns_int(
    value: str, default: Optional[int], monkeypatch
) -> None:
    if value:
        os.environ['ANY_VARIABLE'] = value
    result: Optional[int] = get_integer_or_none('ANY_VARIABLE', default=default)

    if value:
        del os.environ['ANY_VARIABLE']

    assert isinstance(result, int)
    if default:
        assert result == default


@mark.parametrize(
    'wrong_value, default',
    [('10.0', None), ('10_000.0', 100), ('ten', 100.0), (None, 100.0)],
)
def test_get_integer_or_none_returns_none(
    wrong_value: str, default: Optional[int], monkeypatch
) -> None:
    if wrong_value:
        os.environ['ANY_VARIABLE'] = wrong_value
    result: Optional[int] = get_integer_or_none('ANY_VARIABLE', default=default)

    if wrong_value:
        del os.environ['ANY_VARIABLE']

    assert result is None
