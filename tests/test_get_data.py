from pytest import fixture, raises
from unittest.mock import MagicMock

from src.get_data import PostalCodeData
from tests.setup import setup_codes


@fixture()
def setup_obj(setup_codes: list[str], monkeypatch) -> PostalCodeData:
    mock_get_list = MagicMock(return_value=setup_codes)
    monkeypatch.setattr('src.get_data.PostalCodeData.get_list', mock_get_list)
    data: PostalCodeData = PostalCodeData(path='whatever.xlsx', colname='any_name')
    return data


def test_get_list(setup_obj: PostalCodeData, setup_codes: list[str]) -> None:
    data: PostalCodeData = setup_obj
    codes = data.get_list()
    assert isinstance(codes, list)
    assert codes == setup_codes


def test_sample(setup_obj: PostalCodeData, setup_codes: list[str]) -> None:
    data: PostalCodeData = setup_obj
    size: int = len(data.all_codes) - 3
    sample: list[str] = data.sample(size=size)
    mismatches: list[str] = [elem for elem in sample if elem not in setup_codes]
    assert isinstance(sample, list), 'Sample is not a list'
    assert sorted(set(sample)) == sorted(sample), 'Sample values are not unique'
    assert len(sample) == size, 'Sample length is not correct'
    assert len(mismatches) == 0


def test_oversized_sample_raises_error(setup_obj: PostalCodeData) -> None:
    data: PostalCodeData = setup_obj
    size: int = len(data.all_codes) + 5
    with raises(ValueError):
        data.sample(size=size)


def test_sample_from_empty_list(setup_obj: PostalCodeData) -> None:
    data: PostalCodeData = setup_obj
    size: int = len(data.all_codes) - 3
    with raises(ValueError):
        data.sample(size=size, codes=[])
