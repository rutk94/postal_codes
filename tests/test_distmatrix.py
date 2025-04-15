import random
import pgeocode
import numpy as np
from pytest import fixture, mark, raises
from typing import TYPE_CHECKING, Literal, Any

from src.distmatrix import DistanceMatrix
from tests.setup import setup_codes

if TYPE_CHECKING:
    import pandas as pd

@fixture(scope='session')
def setup_obj(setup_codes: list[str]) -> DistanceMatrix:
    distmatrix: DistanceMatrix = DistanceMatrix()
    proper_codes: list[str] = setup_codes[:17]
    _: pd.DataFrame = distmatrix.generate(
        codes=proper_codes, dist_unit='m', codes_col='kod'
    )
    yield distmatrix


def test_codes_checker(setup_codes: list[str]) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    proper_codes: list[str] = distmatrix._check(codes=setup_codes)
    assert proper_codes == setup_codes[:17]
    assert distmatrix.proper_codes == setup_codes[:17]
    assert distmatrix.unknown_codes == [setup_codes[17]]
    assert distmatrix.wrong_format_codes == [setup_codes[18]]


@mark.parametrize('dist_unit, codes_col', [('km', 'kod_pocztowy'), ('m', 'kod')])
def test_distmatrix_genarator(
    setup_codes: list[str], dist_unit: Literal['km', 'm'], codes_col: str
) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    proper_codes: list[str] = sorted(setup_codes[:17])
    matrix: pd.DataFrame = distmatrix.generate(
        codes=setup_codes, dist_unit=dist_unit, codes_col=codes_col
    )

    assert matrix.equals(distmatrix.df)
    assert list(matrix.columns) == proper_codes
    assert list(matrix.index) == proper_codes
    assert list(matrix.select_dtypes(include='int32').columns) == list(matrix.columns)

    random_codes: list[str] = random.choices(proper_codes, k=2)

    # check if distance between the same postal codes equals 0
    diagonal_value: Any = matrix.loc[random_codes[0], random_codes[0]]
    assert isinstance(diagonal_value, (int, np.int32))
    assert diagonal_value == 0

    # check if distance between random postal codes is proper
    distance_value: Any = matrix.loc[random_codes[0], random_codes[1]]
    geodist = pgeocode.GeoDistance('pl')
    factor: int = 1000 if dist_unit == 'm' else 1
    proper_dist: float = geodist.query_postal_code(random_codes[0], random_codes[1])
    proper_dist_int: int = round(proper_dist * factor)
    assert isinstance(distance_value, (int, np.int32))
    assert distance_value == proper_dist_int


@mark.parametrize('dist_unit', ['ft', 'in', 'cm', 'mi', 'metr', 'kilometr', 'k'])
def test_distmatrix_generator_raises_error(
    setup_codes: list[str], dist_unit: Literal['km', 'm']
) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    with raises(ValueError):
        distmatrix.generate(codes=setup_codes, dist_unit=dist_unit)


def test_get_matrix_id(setup_obj: DistanceMatrix, setup_codes: list[str]) -> None:
    code: str = setup_codes[0]
    matrix_id: int = setup_obj.get_matrix_id(code)

    assert isinstance(matrix_id, int)
    assert matrix_id <= len(setup_obj.df)
    assert list(setup_obj.df.columns)[matrix_id] == code


def test_get_matrix_id_raises_attribute_error(setup_codes: list[str]) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    with raises(AttributeError):
        _ = distmatrix.get_matrix_id(code=setup_codes[0])


def test_get_matrix_id_raises_value_error(setup_obj: DistanceMatrix) -> None:
    with raises(ValueError):
        _ = setup_obj.get_matrix_id(code='XX-XXX')
