from pytest import fixture
from typing import TYPE_CHECKING

from src.distmatrix import DistanceMatrix
from src.vehicles import Vehicle, get_vehicles, set_capacities, set_possible_codes
from tests.test_distmatrix import setup_obj as setup_distmatrix  # noqa
from tests.setup import setup_codes, setup_vehicle_codes  # noqa

if TYPE_CHECKING:
    import pandas as pd


@fixture(scope='session')
def setup_vehicles(
    setup_codes: list[str],
    setup_vehicle_codes: tuple[str, ...],
    setup_distmatrix: DistanceMatrix,
) -> list[Vehicle]:
    vehicles: list[Vehicle] = get_vehicles(
        codes=setup_codes,
        vehicle_codes=setup_vehicle_codes,
        dist_matrix=setup_distmatrix,
    )
    return vehicles


def test_get_vehicles(setup_vehicles: list[Vehicle], setup_codes: list[str]) -> None:
    vehicle_nrs: list[int] = [vehicle.vehicle_id for vehicle in setup_vehicles]

    assert sorted(vehicle_nrs) == sorted(set(vehicle_nrs))
    assert all(vehicle.code in setup_codes for vehicle in setup_vehicles)
    assert all(
        setup_vehicles[i].code_id == setup_codes.index(setup_vehicles[i].code)
        for i in range(len(setup_vehicles))
    )


def test_set_capacities(setup_vehicles: list[Vehicle]) -> None:
    set_capacities(amount_cases=100, vehicles=setup_vehicles, factor=1.1)
    capacities: list[int] = [vehicle.capacity for vehicle in setup_vehicles]

    assert len(capacities) != 0
    assert len(capacities) == len(setup_vehicles)
    assert all(isinstance(value, int) for value in capacities)
    assert all(
        capacities[i] == setup_vehicles[i].capacity for i in range(len(capacities))
    )

    # check if all capacities are equal
    assert len(set(capacities)) == 1


def test_set_possible_codes(
    setup_vehicles: list[Vehicle],
    setup_codes: list[str],
    setup_distmatrix: DistanceMatrix,
) -> None:
    dist_matrix: pd.DataFrame = DistanceMatrix().generate(codes=setup_codes)
    set_possible_codes(vehicles=setup_vehicles, dist_matrix=dist_matrix)
    codes: list[str] = [vehicle.code for vehicle in setup_vehicles]
    for vehicle in setup_vehicles:
        code: str = vehicle.code
        other_vehicles_codes = [
            other_code for other_code in codes if other_code != code
        ]
        assert code in vehicle.possible_codes
        assert all(code not in other_vehicles_codes for code in vehicle.possible_codes)
