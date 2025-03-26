from src.vehicles import get_vehicles, Vehicle


def test_get_vehicles() -> None:
    codes: list[str] = [
        '02-777',  # 1 (0)
        '02-232',  # 2 (1)
        '05-500',  # 3 (2)
        '41-300',  # 4 (3)
        '62-510',  # 5 (4)
        '57-432',  # 6 (5)
        '16-070',  # 7 (6)
    ]
    vehicle_codes: tuple[str, ...] = (
        '05-500',  # 3 (2)
        '41-300',  # 4 (3)
        '62-510',  # 5 (4)
    )
    vehicles: list[Vehicle] = get_vehicles(codes=codes, vehicle_codes=vehicle_codes)

    vehicle_nrs: list[int] = [vehicle.nr for vehicle in vehicles]
    assert sorted(vehicle_nrs) == sorted(set(vehicle_nrs))
    assert all(vehicle.code in codes for vehicle in vehicles)
    assert all(
        vehicles[i].code_id == codes.index(vehicles[i].code)
        for i in range(len(vehicles))
    )
