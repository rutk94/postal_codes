import pandas as pd

from src.solver_ortools import Solver
from src.vehicles import Vehicle


class Results:
    """
    Represents calculation results

    Attributes:
        solver: Solver
            Solver object
        vehicles: list[Vehicle]
            List of vehicle objects
        codes: list[str]
            List of all postal codes
    """

    def __init__(
        self, solver: Solver, vehicles: list[Vehicle], codes: list[str]
    ) -> None:
        self.solver: Solver = solver
        self.vehicles: list[Vehicle] = vehicles
        self.codes: list[str] = codes

    def get_matching_result(
        self,
        vehicle_id_colname: str = 'VEHICLE_NR',
        matched_code_colname: str = 'CASE_POSTAL_CODE',
    ) -> pd.DataFrame:
        """
        Returns results of matching vehicles to cases (postal codes)

        Args:
            vehicle_id_colname: str
                Name of column with vehicle identification
            matched_code_colname: str
                Name of columny with postal code matched to vehicle
        Returns:
            match_result_df: pd.DataFrame
                DataFrame with results of matching vehicles to cases (postal codes)
        """
        all_nrs: list[int] = []
        all_codes: list[str] = []
        for i in range(len(self.vehicles)):
            index = self.solver.routing.Start(i)
            nr: int = self.vehicles[i].nr

            while not self.solver.routing.IsEnd(index):
                node_index: int = self.solver.manager.IndexToNode(index)
                case_code: str = self.codes[node_index]
                all_nrs.append(nr)
                all_codes.append(case_code)
                index = self.solver.solution.Value(self.solver.routing.NextVar(index))

        match_result_df: pd.DataFrame = pd.DataFrame(
            {vehicle_id_colname: all_nrs, matched_code_colname: all_codes}
        )

        return match_result_df
