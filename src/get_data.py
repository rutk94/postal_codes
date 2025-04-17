import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional

from src.settings import POSTAL_CODES_PATH, SEED


class PostalCodeData:
    def __init__(
        self, path: str | Path = POSTAL_CODES_PATH, colname: str = 'Kod'
    ) -> None:
        self.path: str | Path = path
        if isinstance(self.path, str):
            self.path = Path(self.path)

        self.colname: str = colname
        self.all_codes: list[str] = self._get_list()

    def _get_list(self) -> list[str]:
        """
        Returns all postal codes from data file.

        Returns:
            codes (list[str]): List of postal codes from data file
        """

        codes_df: pd.DataFrame = pd.read_excel(self.path, usecols=[self.colname])
        codes: list[str] = codes_df[self.colname].tolist()
        return codes

    def sample(
        self, size: int, codes: Optional[list[str]] = None, seed: Optional[int] = SEED
    ) -> list[str]:
        """
        Generates list of postal codes choosed randomly from codes_list.

        Args:
            size (int): Size of random sample list
            codes (Optional[list[str]]): Entry list of postal codes to generate a sample from
            seed (Optional[int], default: env. variable `SEED`): Random seed for sample generator

        Returns:
            sample_list (list[int]): Generated list of postal codes choosed randomly.
                If size == len(codes_list), returns codes_list

        Raises:
            ValueError: If codes_list is empty
            ValueError: If size > len(codes_list)
        """

        codes_list: list[str] = codes if codes is not None else self.all_codes

        if len(codes_list) == 0:
            raise ValueError(f"{codes_list=}, list mustn't be empty")

        if size > len(codes_list):
            raise ValueError(f'{size=} > {len(codes_list)=}')
        elif size == len(codes_list):
            return codes_list
        else:
            if seed:
                np.random.seed(seed)
            codes_array: np.ndarray = np.array(codes_list)
            sample_array: np.ndarray = np.random.choice(
                codes_array, size=size, replace=False
            )
            sample: str | list[str] = sample_array.tolist()
            sample_list: list[str]
            sample_list = list(sample) if isinstance(sample, str) else sample

            return sample_list
