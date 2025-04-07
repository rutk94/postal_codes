import time
import pandas as pd
from pathlib import Path

from src.get_data import PostalCodeData
from src.distmatrix import DistanceMatrix
from src.vehicles import Vehicle, get_vehicles
from src.solver_ortools import Solver, NoSolutionError
from src.results import Results
from src.settings import (
    POSTAL_CODES_PATH,
    OUTPUT_DIR,
    MAX_TOTAL_DISTANCE,
    SOLUTION_LIMIT,
    TIME_LIMIT
)


def main():
    # get postal codes data
    data: PostalCodeData = PostalCodeData(path=POSTAL_CODES_PATH)
    sample: list[str] = sorted(set(data.sample(size=300)))

    # generate distance matrix
    dist_matrix_obj: DistanceMatrix = DistanceMatrix()
    dist_matrix_df: pd.DataFrame = dist_matrix_obj.generate(codes=sample, set_index_enabled=True)
    codes: list[str] = dist_matrix_obj.proper_codes

    # get vehicles list
    vehicle_codes: tuple[str, ...] = tuple(data.sample(size=20, codes=codes))
    vehicles: list[Vehicle] = get_vehicles(codes=codes, vehicle_codes=vehicle_codes)
    starts: list[str] = [vehicle.code_id for vehicle in vehicles]

    # initiate solution
    solver: Solver = Solver(
        dist_matrix=dist_matrix_df.to_numpy().tolist(),
        amount=len(vehicles),
        starts=starts,
        ends=starts,
        max_total_distance=MAX_TOTAL_DISTANCE,
        time_limit=TIME_LIMIT,
        solution_limit=SOLUTION_LIMIT
    )

    try:
        _ = solver.solve()
    except NoSolutionError:
        print('No solution!')
        return
    else:
        # show results
        results: Results = Results(
            solver=solver,
            vehicles=vehicles,
            codes=codes
        )
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