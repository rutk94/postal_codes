import os
from pytest import mark, raises
from typing import Optional

from src.settings_func import get_integer_or_none, get_integer_or_die, get_float_or_die


@mark.parametrize('value', [None, '10'])
def test_get_integer_or_none(value: Optional[str]) -> None:
    var_name: str = 'INTEGER_OR_NONE_VARIABLE'

    if value:
        os.environ[var_name] = value

    result: Optional[int] = get_integer_or_none(var_name)

    if value:
        del os.environ[var_name]
        assert isinstance(result, int)
    else:
        assert result is None


@mark.parametrize('value, default', [('10', None), ('10_000', None), (None, 100)])
def test_get_integer_or_die_returns_int(
    value: Optional[str], default: Optional[int], monkeypatch
) -> None:
    var_name: str = 'INTEGER_VARIABLE'

    if value:
        os.environ[var_name] = value
    result: int = get_integer_or_die(var_name, default=default)

    if value:
        del os.environ[var_name]

    assert isinstance(result, int)
    if default:
        assert result == default


@mark.parametrize(
    'wrong_value, default',
    [('10.0', None), ('10_000.0', 100), ('ten', 100.0), (None, 100.0), (None, '100')],
)
def test_get_integer_or_die_raises_value_error(
    wrong_value: Optional[str], default: Optional[int], monkeypatch
) -> None:
    var_name: str = 'WRONG_INTEGER_VARIABLE'

    if wrong_value:
        os.environ[var_name] = wrong_value

    with raises(ValueError):
        get_integer_or_die(var_name, default=default)

    if wrong_value:
        del os.environ[var_name]


@mark.parametrize('value, default', [('10', None), ('10_000.0', None), (None, 100.0)])
def test_get_float_or_die_returns_int(
    value: Optional[str], default: Optional[float], monkeypatch
) -> None:
    var_name: str = 'FLOAT_VARIABLE'

    if value:
        os.environ[var_name] = value
    result: float = get_float_or_die(var_name, default=default)

    if value:
        del os.environ[var_name]

    assert isinstance(result, float)
    if default:
        assert result == default


@mark.parametrize(
    'wrong_value, default',
    [('10,0', None), ('1-000', '100'), ('ten', 100.0), (None, '100.0')],
)
def test_get_float_or_die_raises_value_error(
    wrong_value: Optional[str], default: Optional[float], monkeypatch
) -> None:
    var_name: str = 'WRONG_FLOAT_VARIABLE'

    if wrong_value:
        os.environ[var_name] = wrong_value

    with raises(ValueError):
        get_float_or_die(var_name, default=default)

    if wrong_value:
        del os.environ[var_name]
