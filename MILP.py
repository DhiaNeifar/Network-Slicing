import numpy as np
import pulp


def generate_random_values(low, high, size):
    return np.random.randint(low=low, high=high, size=size, dtype=int)


def test_solution(_solution, _required_cpus, _total_available_cpus):

    solution = np.sum(np.sum(_required_cpus[:, :, np.newaxis] * _solution, axis=0), axis=0)

    # Test if constraint 1 is verified
    verification = 'verified' if np.all(solution <= _total_available_cpus) else 'unverified'
    Constraint_1 = 'Constraint 1 is ' + verification
    print(Constraint_1)

    # Test if constraint 2 is verified
    print(_total_available_cpus)
    print(_required_cpus)
    print(_solution)
    pass


def network_slicing(_number_NFVs, _number_slices, _total_number_centers, _required_cpus, _total_available_cpus):
    problem = pulp.LpProblem('Network_Slicing', pulp.LpMaximize)

    VNFs_placements = np.array([[[pulp.LpVariable(f'center_{k}_slice_{j}_VNF_{i}', cat='Binary')
                                  for k in range(_total_number_centers)]
                                 for i in range(_number_NFVs)]
                                for j in range(_number_slices)])

    # Maximization Problem
    problem += pulp.LpAffineExpression([(VNFs_placements[j, i, k], _required_cpus[j, i])
                                        for k in range(_total_number_centers)
                                        for i in range(_number_NFVs)
                                        for j in range(_number_slices)]), 'Objective'

    # Constraints
    constraint = 0

    # Constraint 1: CPU utilization does not exceed available CPU
    for k in range(_total_number_centers):
        problem += (pulp.LpAffineExpression([(VNFs_placements[j, i, k], _required_cpus[j, i])
                                            for i in range(_number_NFVs)
                                            for j in range(_number_slices)]) <= _total_available_cpus[k],
                    f'Constraint {constraint}')
        constraint += 1

    # Constraint 2: Each VNF is implemented once
    for i in range(_number_NFVs):
        for k in range(_total_number_centers):
            problem += (pulp.LpAffineExpression(
                [(VNFs_placements[j, i, k], 1) for j in range(_number_slices)]) <= 1, f'Constraint {constraint}')
            constraint += 1

    # Constraint 3: Either all the slice is implemented or not

    # Solve
    problem.solve()
    solution = np.vectorize(pulp.value)(VNFs_placements)
    return solution
    pass


def main():
    # Define topology
    number_edge = 2
    number_cloud = 3
    total_number_centers = number_cloud + number_edge
    available_edge_cpus = generate_random_values(10, 41, number_edge)
    available_cloud_cpus = generate_random_values(20, 201, number_cloud)
    total_available_cpus = np.concatenate((available_edge_cpus, available_cloud_cpus), axis=0)

    # Define slices
    number_slices = 3
    number_NFVs = 4
    required_cpus = generate_random_values(1, 21, (number_slices, number_NFVs))
    solution = network_slicing(number_NFVs, number_slices, total_number_centers, required_cpus, total_available_cpus)
    test_solution(solution, required_cpus, total_available_cpus)
    pass


if __name__ == '__main__':
    main()
