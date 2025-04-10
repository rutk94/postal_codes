from pytest import fixture

from src.vehicles import Vehicle, get_vehicles, get_capacities


@fixture
def setup_codes() -> list[str]:
    return [
        '02-777',  # 1 (0)
        '02-232',  # 2 (1)
        '05-500',  # 3 (2)
        '41-300',  # 4 (3)
        '62-510',  # 5 (4)
        '57-432',  # 6 (5)
        '16-070',  # 7 (6)
    ]


@fixture
def setup_vehicle_codes() -> tuple[str, ...]:
    return (
        '05-500',  # 3 (2)
        '41-300',  # 4 (3)
        '62-510',  # 5 (4)
    )


def test_get_vehicles(setup_codes: list[str], setup_vehicle_codes: tuple[str, ...]) -> None:
    vehicles: list[Vehicle] = get_vehicles(
        codes=setup_codes, vehicle_codes=setup_vehicle_codes
    )
    vehicle_nrs: list[int] = [vehicle.nr for vehicle in vehicles]

    assert sorted(vehicle_nrs) == sorted(set(vehicle_nrs))
    assert all(vehicle.code in setup_codes for vehicle in vehicles)
    assert all(
        vehicles[i].code_id == setup_codes.index(vehicles[i].code)
        for i in range(len(vehicles))
    )


def test_get_capacities(
    setup_codes: list[str], setup_vehicle_codes: tuple[str, ...]
) -> None:
    vehicles: list[Vehicle] = get_vehicles(
        codes=setup_codes, vehicle_codes=setup_vehicle_codes
    )
    capacities: list[int] = get_capacities(
        amount_cases=100, vehicles=vehicles, factor=1.1
    )

    assert len(capacities) != 0
    assert len(capacities) == len(vehicles)
    assert all(isinstance(value, int) for value in capacities)
    assert all(capacities[i] == vehicles[i].capacity for i in range(len(capacities)))

    # check if all capacities are equal
    assert len(set(capacities)) == 1
