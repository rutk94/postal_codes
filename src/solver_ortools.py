from ortools.constraint_solver import routing_enums_pb2, pywrapcp


class NoSolutionError(Exception):
    pass


class Solver:
    def __init__(
        self,
        dist_matrix: list,
        amount: int,
        starts: list,
        ends: list,
        # nodes: list,
        # capacities: list[int],

        # TODO: add global variables
        # max_single_distance_enabled: bool = True,  # MAX_SINGLE_DISTANCE_ENABLED
        max_total_distance: int = 10_000_000,   # MAX_DISTANCE
        time_limit: int = 60,    # TIME_LIMIT
        solution_limit: int = 10_000_000,   # SOLUTION_LIMIT
    ) -> None:

        self.dist_matrix: list = dist_matrix
        self.amount: int = amount
        self.starts: list = starts
        self.ends: list = ends
        # self.nodes: list = nodes
        # self.capacities: list[int] = capacities

        # self.max_single_distance_enabled: bool = max_single_distance_enabled
        self.max_total_distance: int = max_total_distance
        self.time_limit: int = time_limit
        self.solution_limit: int = solution_limit

        self.manager = pywrapcp.RoutingIndexManager(
            # len(self.nodes),
            len(self.dist_matrix),
            self.amount,
            self.starts,
            self.ends
        )
        self.routing = pywrapcp.RoutingModel(self.manager)

        # if max_single_distance_enabled:
        #     for node in self.nodes:
        #         self.routing.SetAllowedVehiclesForIndex(
        #             vehicles=node.possible_employees_nrs,
        #             index=self.manager.NodeToIndex(node.node_id)
        #         )

        # placeholder
        self.solution = None

    def _distance_callback(self, from_index, to_index):
        """Returns distance between two points"""
        # TODO: finish function
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        # index_from = self.nodes[from_node].matrix_id
        # index_to = self.nodes[to_node].matrix_id
        # return self.dist_matrix[index_from][index_to]
        return self.dist_matrix[from_node][to_node]

    def _distance_callback_symmetrical(self, from_index, to_index):
        """Returns minimal distance between two points"""
        return min(
            self._distance_callback(from_index, to_index),
            self._distance_callback(to_index, from_index)
        )

    # def _demand_callback(self, from_index):
    #     """Returns demand at given point"""
    #     # TODO: finish function
    #     from_node = self.manager.IndexToNode(from_index)
    #     # return self.nodes[from_node].demand_weight
    #     pass


    def solve(self):
        # add distance dimension
        transit_callback_index = self.routing.RegisterTransitCallback(
            self._distance_callback_symmetrical
        )
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        self.routing.AddDimension(
            evaluator_index=transit_callback_index,
            slack_max=0,
            capacity=self.max_total_distance,
            fix_start_cumul_to_zero=True,
            name='distance'
        )
        distance_dimension = self.routing.GetDimensionOrDie('distance')
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # # add capacity dimension
        # demand_callback_index = self.routing.RegisterUnaryTransitCallback(self._demand_callback)
        # self.routing.AddDimensionWithVehicleCapacity(
        #     evaluator_index=demand_callback_index,
        #     slack_max=0,
        #     vehicle_capacities=self.capacities,
        #     fix_start_cumul_to_zero=True,
        #     name='capacity'
        # )

        # define parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.seconds = self.time_limit
        search_parameters.solution_limit = self.solution_limit

        # calculate solution
        self.solution = self.routing.SolveWithParameters(search_parameters)

        # return solution or raise error
        if self.routing.status() == 1:
            return self.solution
        else:
            # TODO: add dictionary of statuses from: developers.google.com/optimization/routing/routing_options
            print(self.routing.status())
            raise NoSolutionError('Solver couldn\'t find any solution!')
