import time
from pathlib import Path

from src.get_data import PostalCodeData
from src.distmatrix import DistanceMatrix
from src.vehicles import Vehicle, get_vehicles, set_capacities, set_possible_codes
from src.nodes import Node, get_nodes
from src.solver_ortools import Solver, NoSolutionError
from src.results import Results
from src.settings import (
    POSTAL_CODES_PATH,
    OUTPUT_DIR,
    MAX_TOTAL_DISTANCE,
    SOLUTION_LIMIT,
    TIME_LIMIT,
    CAPACITY_FACTOR,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def main():
    # get data
    data: PostalCodeData = PostalCodeData(path=POSTAL_CODES_PATH)
    sample: list[str] = sorted(set(data.sample(size=300)))
    vehicle_codes: tuple[str, ...] = tuple(data.sample(size=20, seed=4321))

    # generate distance matrix
    dist_matrix_obj: DistanceMatrix = DistanceMatrix()
    dist_matrix_df: pd.DataFrame = dist_matrix_obj.generate(
        codes=sample + list(vehicle_codes)
    )

    # get proper postal codes
    codes: list[str] = dist_matrix_obj.proper_codes
    vehicle_codes = tuple([code for code in vehicle_codes if code in codes])

    # get vehicles list
    vehicles: list[Vehicle] = get_vehicles(
        codes=codes, vehicle_codes=vehicle_codes, dist_matrix=dist_matrix_obj
    )
    starts: list[str] = [vehicle.matrix_id for vehicle in vehicles]

    # set capacities for each vehicle
    set_capacities(
        amount_cases=len(codes), vehicles=vehicles, factor=CAPACITY_FACTOR
    )
    capacities: list[int] = [vehicle.capacity for vehicle in vehicles]

    # set possible codes for each vehicle
    set_possible_codes(
        vehicles=vehicles,
        dist_matrix=dist_matrix_df
    )

    # get nodes list
    nodes: list[Node] = get_nodes(
        codes=codes,
        vehicles=vehicles,
        dist_matrix=dist_matrix_obj
    )

    # initiate solution
    solver: Solver = Solver(
        dist_matrix=dist_matrix_df.to_numpy().tolist(),
        amount=len(vehicles),
        starts=starts,
        ends=starts,
        nodes=nodes,
        capacities=capacities,
        max_total_distance=MAX_TOTAL_DISTANCE,
        time_limit=TIME_LIMIT,
        solution_limit=SOLUTION_LIMIT,
    )

    try:
        solver.solve()
    except NoSolutionError:
        print('No solution!')
        return
    else:
        # show results
        results: Results = Results(solver=solver, vehicles=vehicles, codes=codes)
        if not OUTPUT_DIR.exists():
            Path.mkdir(OUTPUT_DIR, parents=True)
        results.get_matching_result().to_excel(OUTPUT_DIR / 'matching.xlsx')
        results.get_map_result(OUTPUT_DIR / 'map.png')
        return


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print(stop - start)
