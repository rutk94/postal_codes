from src.vehicles import Vehicle
from src.distmatrix import DistanceMatrix


class Node:
    def __init__(
        self,
        node_id: int,
        matrix_id: int,
        code: str,
        demand: int,
        is_vehicle: bool,
        is_case: bool,
        possible_vehicles: list[Vehicle],
    ) -> None:
        """
        Represents Node object.

        Args:
            node_id (int): Node identity number
            matrix_id (int): Node index number in distance matrix
            code (str): Postal code of Node
            demand (int): Amount of cases in Node
            is_vehicle (bool): True / False if Node is vehicle
            is_case (bool): True / False if Node is case
            possible_vehicles (list[Vehicle]): List of Vehicle objects available for Node
        """

        self.node_id: int = node_id
        self.matrix_id: int = matrix_id
        self.code: str = code
        self.demand: int = demand
        self.is_vehicle: bool = is_vehicle
        self.is_case: bool = is_case
        self.possible_vehicles: list[Vehicle] = possible_vehicles


def get_nodes(
    codes: list[str], vehicles: list[Vehicle], dist_matrix: DistanceMatrix
) -> list[Node]:
    """
    Returns a list of Node objects.

    Args:
        codes (list[str]): List of postal codes
        vehicles (list[Vehicle]): List of Vehicle objects
        dist_matrix (DistanceMatrix): DistanceMatrix object

    Returns:
        nodes (List[Node]): List of Node objects
    """

    vehicle_codes: list[str] = [vehicle.code for vehicle in vehicles]

    nodes: list[Node] = []
    for i in range(len(codes)):
        node_id: int = i
        code: str = codes[i]
        matrix_id: int = dist_matrix.get_matrix_id(code=code)
        demand: int = 1
        is_vehicle: bool = code in vehicle_codes
        is_case: bool = code in codes
        if not is_vehicle and not is_case:
            raise ValueError

        possible_vehicles: list[Vehicle]
        if is_vehicle:
            possible_vehicles = [
                vehicle for vehicle in vehicles if vehicle.code == code
            ]
        else:
            possible_vehicles = [
                vehicle for vehicle in vehicles if code in vehicle.possible_codes
            ]

        node: Node = Node(
            node_id=node_id,
            matrix_id=matrix_id,
            code=code,
            demand=demand,
            is_vehicle=is_vehicle,
            is_case=is_case,
            possible_vehicles=possible_vehicles,
        )
        nodes.append(node)

    return nodes
