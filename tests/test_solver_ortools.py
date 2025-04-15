from pytest import fixture, raises, mark
from unittest.mock import MagicMock
from typing import Any

from src.solver_ortools import Solver, NoSolutionError
from tests.test_nodes import Node, setup_nodes
from tests.test_vehicles import setup_vehicles  # noqa
from tests.test_distmatrix import setup_obj as setup_distmatrix # noqa
from tests.setup import setup_solver_data, setup_codes, setup_vehicle_codes # noqa


@fixture(scope='session')
def setup_solver(
    request, setup_solver_data: dict[str, Any], setup_nodes: list[Node]
) -> Solver:
    solver: Solver = Solver(
        dist_matrix=setup_solver_data['dist_matrix'],
        amount=setup_solver_data['amount'],
        starts=setup_solver_data['starts'],
        ends=setup_solver_data['ends'],
        nodes=setup_nodes,
        capacities=setup_solver_data['capacities'],
        max_single_distance_enabled=request,
        max_total_distance=10_000_000,
        time_limit=10,  # duration on fixture creation
        solution_limit=10_000_000
    )
    solver.solve()
    yield solver

@mark.parametrize('setup_solver', [[True, False]], indirect=True)
def test_solve(setup_solver: Solver) -> None:
    assert setup_solver.solution is not None


def test_solver_raises_no_solution_error(setup_solver: Solver, monkeypatch) -> None:
    mock_status = MagicMock(return_value=None)
    monkeypatch.setattr(
        'ortools.constraint_solver.pywrapcp.RoutingModel.SolveWithParameters',
        mock_status,
    )
    with raises(NoSolutionError):
        setup_solver.solve()
