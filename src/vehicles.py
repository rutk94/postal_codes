import math
from pydantic import BaseModel

from src.settings import CAPACITY_FACTOR


VEHICLE_CODES: tuple[str, ...] = ('05-500', '41-300', '62-510')


class Vehicle(BaseModel):
    """
    Represents vehicle attributes.

    Attributes:
        nr: int
            Number of vehicle
        code: str
            Postal code of vehicle
        code_id: int
            Index number of vehicle postal code in the list of all postal codes
    """

    nr: int
    code: str
    code_id: int
    capacity: int = 0  # set by calling get_capacity()


def get_vehicles(
    codes: list[str], vehicle_codes: tuple[str, ...] = VEHICLE_CODES
) -> list[Vehicle]:
    """
    Returns list of Vehicle objects.

    Args:
        codes: list[str]
            List of all postal codes
        vehicle_codes: tuple[str, ...]
            List of vehicles postal codes
    Returns:
        vehicles: list[Vehicle]
            List of Vehicle objects
    """

    vehicles: list[Vehicle] = [
        Vehicle(nr=i, code=vehicle_codes[i], code_id=codes.index(vehicle_codes[i]))
        for i in range(len(vehicle_codes))
    ]

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
    value: int = int(math.ceil(amount_cases / len(vehicles) * factor))

    # # check if value is smaller then max_demand
    # if value >= max_demand:
    #     value = max_demand

    # actualize Vehicle attribute
    for vehicle in vehicles:
        vehicle.capacity = value

    # generate capacities list
    capacities: list[int] = [vehicle.capacity for vehicle in vehicles]

    return capacities
