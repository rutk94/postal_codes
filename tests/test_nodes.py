from pytest import fixture

from src.vehicles import Vehicle
from src.distmatrix import DistanceMatrix
from src.nodes import Node, get_nodes
from tests.test_vehicles import setup_vehicles
from tests.test_distmatrix import setup_obj as setup_distmatrix
from tests.setup import setup_codes, setup_vehicle_codes    # noqa


@fixture(scope='session')
def setup_nodes(
    setup_codes: list[str],
    setup_vehicles: list[Vehicle],
    setup_distmatrix: DistanceMatrix
) -> list[Node]:
    nodes: list[Node] = get_nodes(
        codes=setup_codes[:17], # only proper codes
        vehicles=setup_vehicles,
        dist_matrix=setup_distmatrix,
    )
    yield nodes

def test_get_nodes(setup_nodes: list[Node], setup_codes: list[str]) -> None:
    assert len(setup_nodes) > 0
    assert len(setup_nodes) == len(setup_codes[:17])
    assert all(isinstance(value, Node) for value in setup_nodes)
