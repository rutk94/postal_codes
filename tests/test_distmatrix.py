import random
import numpy as np
import pgeocode
from pytest import fixture, mark, raises
from typing import TYPE_CHECKING, Literal, Any
if TYPE_CHECKING:
    import pandas as pd

from src.distmatrix import DistanceMatrix


@fixture()
def setup_codes_list() -> list[str]:
    # **DO NOT** change order
    # proper values - numbers from 0 to 6
    # unknown value - number 7
    # wrong format value - number 8
    return [
        '02-777',  # 1 (0)
        '02-232',  # 2 (1)
        '05-500',  # 3 (2)
        '41-300',  # 4 (3)
        '62-510',  # 5 (4)
        '57-432',  # 6 (5)
        '16-070',  # 7 (6)
        '99-999',  # 8 (7) - unknown code
        'A00-12',  # 9 (8) - wrong format code
    ]


def test_codes_checker(setup_codes_list: list[str]) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    proper_codes: list[str] = distmatrix._check(codes=setup_codes_list)
    assert proper_codes == setup_codes_list[:7]
    assert distmatrix.proper_codes == setup_codes_list[:7]
    assert distmatrix.unknown_codes == [setup_codes_list[7]]
    assert distmatrix.wrong_format_codes == [setup_codes_list[8]]


@mark.parametrize('dist_unit, codes_col', [('km', 'kod_pocztowy'), ('m', 'kod')])
def test_distmatrix_genarator(
    setup_codes_list: list[str], dist_unit: Literal['km', 'm'], codes_col: str
) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    matrix: pd.DataFrame = distmatrix.generate(
        codes=setup_codes_list, dist_unit=dist_unit, codes_col=codes_col
    )
    assert list(matrix.columns)[0] == codes_col
    assert list(matrix.columns)[1:] == sorted(setup_codes_list[:7])
    assert matrix[codes_col].tolist() == sorted(setup_codes_list[:7])
    assert matrix.equals(distmatrix.df)
    assert list(matrix.select_dtypes(include='int32').columns) == list(
        matrix.columns[1:]
    )

    matrix.set_index(codes_col, inplace=True)
    random_codes: list[str] = random.choices(setup_codes_list[:7], k=2)

    diagonal_value: Any = matrix.loc[random_codes[0], random_codes[0]]
    assert isinstance(diagonal_value, (int, np.int32))
    assert diagonal_value == 0

    distance_value: Any = matrix.loc[random_codes[0], random_codes[1]]
    geodist = pgeocode.GeoDistance('pl')
    factor: int = 1000 if dist_unit == 'm' else 1
    proper_dist: float = geodist.query_postal_code(random_codes[0], random_codes[1])
    proper_dist_int: int = np.round(proper_dist * factor)
    assert isinstance(distance_value, (int, np.int32))
    assert distance_value == proper_dist_int


@mark.parametrize('dist_unit', ['ft', 'in', 'cm', 'mi', 'metr', 'kilometr', 'k'])
def test_distmatrix_generator_raises_error(
    setup_codes_list: list[str], dist_unit: Literal['km', 'm']
) -> None:
    distmatrix: DistanceMatrix = DistanceMatrix()
    with raises(ValueError):
        distmatrix.generate(codes=setup_codes_list, dist_unit=dist_unit)
