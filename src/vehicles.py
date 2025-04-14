from math import ceil
import pandas as pd

from src.distmatrix import DistanceMatrix
from src.settings import CAPACITY_FACTOR


# VEHICLE_CODES: tuple[str, ...] = ('05-500', '41-300', '62-510')


class Vehicle:
    """
    Represents vehicle attributes.

    Attributes:
        vehicle_id: int
            Number of vehicle
        code: str
            Postal code of vehicle
        code_id: int
            Index number of vehicle postal code in the list of all postal codes
    """

    def __init__(
        self, vehicle_id: int, code: str, code_id: int, matrix_id: int, max_dist_from_home: int
    ) -> None:
        self.vehicle_id: int = vehicle_id
        self.code: str = code
        self.code_id: int = code_id
        self.matrix_id: int = matrix_id
        self.max_dist_from_home: int = max_dist_from_home

        # placeholders
        self.capacity: int = 0  # set by calling get_capacities()
        self.possible_codes: list[str] = [code]  # expanded by calling set_possible_codes()


def get_vehicles(
    codes: list[str], vehicle_codes: tuple[str, ...], dist_matrix: DistanceMatrix
) -> list[Vehicle]:
    """
    Returns list of Vehicle objects.

    Args:
        codes: list[str]
            List of all postal codes
        vehicle_codes: tuple[str, ...]
            List of vehicles postal codes
        dist_matrix: DistanceMatrix
            Distances matrix object
    Returns:
        vehicles: list[Vehicle]
            List of Vehicle objects
    """

    vehicles: list[Vehicle] = []
    for i in range(len(vehicle_codes)):
        code: str = vehicle_codes[i]
        code_id: int = codes.index(code)
        matrix_id: int = dist_matrix.get_matrix_id(code)
        vehicle: Vehicle = Vehicle(
            vehicle_id=i,
            code=code,
            code_id=code_id,
            matrix_id=matrix_id,
            # TODO: load max distances individualy for every vehicle
            max_dist_from_home=150_000,
        )
        vehicles.append(vehicle)

    return vehicles


def get_capacities(
    amount_cases: int,
    vehicles: list[Vehicle],
    # max_demand: int
    factor: float = CAPACITY_FACTOR,
) -> list[int]:
    """
    Returns a list of capacity values for each vehicle,
    calculated using the following operation:

    amount_cases / len(vehicles) * factor

    The result is rounded up and changed to "integer" type.
    Each vehicle gets an equal capacity.
    Vehicle objects gets the new attribute 'capacity'.

    Args:
        amount_cases: int
            Amount of all cases
        vehicles: list[Vehicle]
            List of Vehicle objects
        factor: float
            Constant factor used to loosen the range of possibilities

    Returns:
        capacities: list[int]
            List of capacity values for each vehicle
            in order according to Vehicle objects list "vehicles"
    """

    # calculate capacity
    value: int = int(ceil(amount_cases / len(vehicles) * factor))

    # # check if value is smaller then max_demand
    # if value >= max_demand:
    #     value = max_demand

    # actualize Vehicle attribute
    for vehicle in vehicles:
        vehicle.capacity = value

    # # generate capacities list
    # capacities: list[int] = [vehicle.capacity for vehicle in vehicles]
    #
    # return capacities


def set_possible_codes(
    vehicles: list[Vehicle], dist_matrix: pd.DataFrame
) -> list[Vehicle]:
    """
    For every single vehicle sets postal codes which fits in maximum distance range.
    If vehicle.possible_codes is already filled, the vehicle is being omitted.

    Args:
        vehicles: list[Vehicle]
            List of vehicles objects
        dist_matrix: pd.DataFrame
            Distance matrix as dataframe

    Returns:
        actualized_vehicles: list[Vehicle]
            List of actualized vehicles objects

    Sets attributes:
        vehicle.possible_codes: list[str]
    """
    vehicle_codes: list[str] = [vehicle.code for vehicle in vehicles]

    actualized_vehicles: list[Vehicle] = []
    for vehicle in vehicles:
        code: str = vehicle.code
        max_dist: int = vehicle.max_dist_from_home

        if vehicle.possible_codes != [code]:
            continue

        # get vehicle distances to all codes
        vehicle_distances: pd.DataFrame = dist_matrix.loc[code].to_frame()

        # exclude distances to other vehicles
        vehicle_distances: pd.DataFrame = vehicle_distances.drop(vehicle_codes, axis=0)

        # exclude distances greater than max
        vehicle_limited_distances: pd.DataFrame = vehicle_distances[
            vehicle_distances[code] <= max_dist
        ]

        # set possible codes for vehicle
        possible_codes: list[str] = list(vehicle_limited_distances.index)
        vehicle.possible_codes += possible_codes

        actualized_vehicles.append(vehicle)

    # return actualized_vehicles
