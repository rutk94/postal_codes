from pydantic import BaseModel


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


def get_vehicles(
    codes: list[str], vehicle_codes: tuple[str, ...] = VEHICLE_CODES
) -> list[Vehicle]:
    """
    Returns list of Vehicle objects.
    Args:
        codes: list[str]
            List of all postal codes
        vehicle_codes:
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
