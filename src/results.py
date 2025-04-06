import pgeocode
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from src.solver_ortools import Solver
from src.vehicles import Vehicle

if TYPE_CHECKING:
    import numpy as np


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
                Name of column with postal code matched to vehicle
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

    def get_map_result(
        self,
        map_shape_path: Path,
        output_path: Path,
        match_result_df: Optional[pd.DataFrame] = None,
        vehicle_id_colname: str = 'VEHICLE_NR',
        matched_code_colname: str = 'CASE_POSTAL_CODE',
    ) -> None:
        """
        Generates matching results as map plot.

        Args:
            map_shape_path: Path
                Path to map shape file in .geojson format
            output_path: Path
                Path to output file.
            match_result_df: Optional[pd.DataFrame] = None
                DataFrame object with matching results. If None, self.get_matching_result method is used
            vehicle_id_colname: str
                Name of column with vehicle identification
            matched_code_colname: str
                Name of column with postal code matched to vehicle

        Returns:
            None

        Raises:
            ValueError
                if output_path.suffix != '.png'
        """

        nomi = pgeocode.Nominatim('pl')

        # matched codes geopoints
        if not match_result_df:
            match_result_df = self.get_matching_result(
                vehicle_id_colname, matched_code_colname
            )

        match_result_df = match_result_df.reset_index()
        matched_codes_array: np.ndarray = match_result_df.loc[
            :, matched_code_colname
        ].to_numpy()
        match_result_df[['latitude', 'longitude']] = nomi.query_postal_code(
            matched_codes_array
        ).loc[:, ['latitude', 'longitude']]
        match_result_gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(
            match_result_df,
            geometry=gpd.points_from_xy(
                match_result_df['longitude'], match_result_df['latitude']
            ),
            crs='EPSG:4326',
        )

        # vehicles codes geopoints
        vehicles_id_list: list[int] = [vehicle.nr for vehicle in self.vehicles]
        vehicles_df: pd.DataFrame = pd.DataFrame({vehicle_id_colname: vehicles_id_list})
        vehicles_codes_list: list[str] = [vehicle.code for vehicle in self.vehicles]
        vehicles_df[['latitude', 'longitude']] = nomi.query_postal_code(
            vehicles_codes_list
        ).loc[:, ['latitude', 'longitude']]
        vehicles_gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(
            vehicles_df,
            geometry=gpd.points_from_xy(
                vehicles_df['longitude'], vehicles_df['latitude']
            ),
            crs='EPSG:4326',
        )

        # plot
        fig, ax = plt.subplots()
        map_shape = gpd.read_file(map_shape_path)
        map_shape.plot(ax=ax, color='gainsboro', edgecolor='grey').set_axis_off()

        match_result_gdf.plot(
            ax=ax,
            column=vehicle_id_colname,
            legend=True,
            legend_kwds={'loc': 'best'},
            cmap='tab20',
            marker='o',
            markersize=5,
            categorical=True,
            categories=match_result_gdf[vehicle_id_colname].drop_duplicates().tolist(),
        ).set_axis_off()

        vehicles_gdf.plot(
            ax=ax,
            column=vehicle_id_colname,
            legend=True,
            marker='x',
            cmap='tab20',
            markersize=15,
            categorical=True,
            categories=vehicles_gdf[vehicle_id_colname].drop_duplicates().tolist(),
        ).set_axis_off()

        # save to file or show plot
        if isinstance(output_path, str):
            output_path = Path(output_path)

        if output_path.suffix == '':
            if not output_path.exists():
                Path.mkdir(output_path, parents=True)

            output_path = output_path / 'wykres.png'

        if output_path.suffix != '.png':
            raise ValueError(f'Wrong {output_path=}. Should be .png file.')

        if not output_path.parent.exists():
            Path.mkdir(output_path.parent, parents=True)

        plt.savefig(output_path)
