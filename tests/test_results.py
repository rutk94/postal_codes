import pandas as pd
from pytest import fixture

from src.solver_ortools import Solver
from src.vehicles import Vehicle, get_vehicles
from src.results import Results


@fixture()
def setup_solver() -> Solver:
    dist_matrix: list[list[int]] = [
      [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
      [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
      [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
      [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
      [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
      [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
      [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
      [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
      [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
      [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
      [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
      [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
      [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
      [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
      [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
      [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
      [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
    ]
    starts: list[str] = [1, 2, 15, 16]
    ends: list[str] = [1, 2, 15, 16]
    amount: int = len(starts)
    solver: Solver = Solver(
        dist_matrix=dist_matrix,
        amount=amount,
        starts=starts,
        ends=ends,
        time_limit=30
    )
    return solver

@fixture()
def setup_codes() -> list[str]:
    return [
        '05-080',   # 1 (0)
        '05-152',   # 2 (1)
        '05-500',   # 3 (2)
        '41-300',   # 4 (3)
        '62-510',   # 5 (4)
        '05-860',   # 6 (5)
        '14-220',   # 7 (6)
        '41-103',   # 8 (7)
        '62-304',   # 9 (8)
        '99-423',   # 10 (9)
        '01-587',   # 11 (10)
        '02-967',   # 12 (11)
        '05-779',   # 13 (12)
        '06-993',   # 14 (13)
        '41-134',   # 15 (14)
        '66-978',   # 16 (15)
        '90-478',   # 17 (16)
    ]

@fixture()
def setup_vehicles(setup_codes: list[str]) -> list[Vehicle]:
    vehicle_codes: tuple[str, ...] = (
        '05-500',   # 3 (2)
        '41-300',   # 4 (3)
        '62-510',   # 5 (4)
    )
    vehicles: list[Vehicle] = get_vehicles(codes=setup_codes, vehicle_codes=vehicle_codes)
    return vehicles


def test_get_matching_result(setup_solver: Solver, setup_codes: list[str], setup_vehicles: list[Vehicle]) -> None:
    _ = setup_solver.solve()
    results: Results = Results(
        solver=setup_solver,
        vehicles=setup_vehicles,
        codes=setup_codes
    )
    matching_df: pd.DataFrame = results.get_matching_result(
        vehicle_id_colname='vehicle_nr',
        matched_code_colname='postal_code'
    )
    assert isinstance(matching_df, pd.DataFrame)
    assert all(colname in list(matching_df.columns) for colname in ['vehicle_nr', 'postal_code'])
    assert matching_df['postal_code'].is_unique
