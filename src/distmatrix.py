from __future__ import annotations

import re
import pgeocode
import pandas as pd
import numpy as np
from typing import Literal


class DistanceMatrix:
    def __init__(self) -> None:
        # placeholders
        self.df: pd.DataFrame = pd.DataFrame()
        self.proper_codes: list[str] = []
        self.wrong_format_codes: list[str] = []
        self.unknown_codes: list[str] = []

    @classmethod
    def create_from_filepath(cls) -> DistanceMatrix:  # type: ignore[empty-body]
        pass

    @classmethod
    def load_from_database(cls) -> DistanceMatrix:  # type: ignore[empty-body]
        pass

    def _check(self, codes: list[str], setattr_enabled: bool = True) -> list[str]:
        """
        Checks format of postal codes and whether they are available in pgeocode database.
        Args:
            codes: list[str]
                List of postal codes
            setattr_enabled: bool
                If you need to set attributes
                self.proper_codes, self.wrong_format_codes, self.unknown_codes

        Returns:
            proper_codes: list[str]
                List of proper postal codes

        Sets attributes (if setattr_enabled is True):
            self.proper_codes: list[str]
                List of proper postal codes
            self.wrong_format_codes: list[str]
                List of postal codes with wrong format
            self.unknown_codes: list[str]
                List of postal codes which are not available in pgeocode database
        """
        # wrong format codes
        pattern = re.compile(r'\d{2}-\d{3}')
        wrong_format_codes: list[str] = [
            code for code in codes if pattern.match(code) is None
        ]

        # unknown codes
        nomi = pgeocode.Nominatim('pl')
        df_locations: pd.DataFrame = nomi.query_postal_code(codes)
        df_notna: pd.DataFrame = df_locations.dropna(subset=['latitude', 'longitude'])
        known_codes: list[str] = df_notna['postal_code'].tolist()
        unknown_codes: list[str] = [
            code
            for code in codes
            if code not in known_codes and code not in wrong_format_codes
        ]

        # proper codes
        proper_codes: list[str] = [
            code
            for code in codes
            if code not in wrong_format_codes and code not in unknown_codes
        ]

        if setattr_enabled:
            self.wrong_format_codes = wrong_format_codes
            self.unknown_codes = unknown_codes
            self.proper_codes = proper_codes

        return proper_codes

    def generate(
        self,
        codes: list[str],
        dist_unit: Literal['km', 'm'] = 'm',
        codes_col: str = 'KOD_POCZ',
        set_index_enabled: bool = False,
    ) -> pd.DataFrame:
        """
        Generates symmetrical matrix including distances between postal codes, as DataFrame object.
        Args:
            codes: list[str]
                List of postal codes
            dist_unit: Literal['km', 'm'] = 'm'
                Unit of calculated distances: 'km' - kilometers, 'm' - meters
            codes_col: str = 'KOD_POCZ'
                Name of 1st column including postal codes
            set_index_enabled: bool = False
                If you need to represent postal codes as index
        Returns:

        """
        # check provided distance unit
        if dist_unit.lower() not in ['km', 'm']:
            raise ValueError(
                f'Wrong argument value: {dist_unit=}. Should be "km" or "m"'
            )

        # remove duplicates and sort values
        codes: list[str] = sorted(set(codes))

        # check codes
        codes = self._check(codes)

        # define distance unit
        factor: int = 1000 if dist_unit == 'm' else 1

        # generate distance matrix
        geodist = pgeocode.GeoDistance('pl')
        matrix: np.ndarray = np.zeros((len(codes), len(codes)))
        iter_codes: list[str] = codes.copy()
        while iter_codes:
            code: str = iter_codes.pop(0)
            code_rep: list[str] = [code] * len(iter_codes)
            calc: np.ndarray = geodist.query_postal_code(iter_codes, code_rep)
            calc = np.round(calc * factor)
            i: int = codes.index(code)
            matrix[i] = (
                list(calc[:0]) + [0] * (len(codes) - len(iter_codes)) + list(calc[0:])
            )

        # reflect matrix by its diagonal
        matrix += matrix.T

        # create DataFrame object
        matrix_df: pd.DataFrame = pd.DataFrame(matrix, columns=codes, dtype='int32')
        matrix_df.insert(0, codes_col, codes)

        if set_index_enabled:
            matrix_df.set_index(codes_col, inplace=True)

        self.df = matrix_df.copy()

        return matrix_df

    def get_matrix_id(self, code: str) -> int:
        """
        Returns positional number (id) of given code in distance matrix dataframe.

        Args:
            code: str
                Postal code to find in distance matrix dataframe

        Returns:
            matrix_id: int
                Positional number (id) of given code

        Raises:
            AttributeError - if dataframe doesn't exist yet.
            ValueError - if given code doesn't exist in distance matrix
        """
        if self.df.equals(pd.DataFrame()):
            raise AttributeError(
                "DistanceMatrix dataframe doesn't exist yet. "
                'Use method "DistanceMatrix.generate()" to create a dataframe.'
            )

        dist_matrix_codes: list[str] = list(self.df.columns)
        if code not in dist_matrix_codes:
            raise ValueError(f'{code=} not in DistanceMatrix codes.')

        matrix_id: int = dist_matrix_codes.index(code)

        return matrix_id
