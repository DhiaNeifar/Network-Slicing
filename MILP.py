import numpy as np
import pulp


def _print(text, value):
    print(f'\n{text}:\n{value}')


def generate_random_values(low, high, size):
    return np.random.randint(low=low, high=high, size=size, dtype=np.int16)


def test_solution(_solution, _deployed_slices, _required_cpus, _total_available_cpus):
    constraint = 'Constraint'
    consumed_cpu_per_center = np.sum(np.sum(_required_cpus[:, :, np.newaxis] * _solution, axis=0),
                                     axis=0, dtype=np.int16)

    _print('Total Available CPUs', _total_available_cpus)
    _print('Consumed CPU Per Center', consumed_cpu_per_center)

    # Test if constraint 1 is verified
    verification = 'verified' if np.all(consumed_cpu_per_center <= _total_available_cpus) else 'unverified'
    Constraint_1 = f'\n{constraint} 1 is ' + verification
    print(Constraint_1)

    # Test if constraint 2 and 3 are verified
    sums = np.sum(_solution, axis=(1, 2))  # Sum over both rows and columns of each matrix

    # Check if each sum is either 6 or 0
    verification = 'verified' if np.all(np.logical_or(sums == _solution.shape[1], sums == 0)) else 'unverified'
    Constraint_2_3 = f'\n{constraint} 2 & 3 are ' + verification
    print(Constraint_2_3)

    _print('Deployed Slices', _deployed_slices)
    _print('Solution', _solution)


def define_topology(number_edge=2, number_cloud=3):
    _number_edge = number_edge
    _number_cloud = number_cloud
    _total_number_centers = _number_cloud + _number_edge
    available_edge_cpus = generate_random_values(10, 41, number_edge)
    available_cloud_cpus = generate_random_values(20, 201, number_cloud)
    _total_available_cpus = np.concatenate((available_edge_cpus, available_cloud_cpus), axis=0, dtype=np.int16)
    return _total_number_centers, _total_available_cpus


def define_slices(number_slices=1, number_VNFs=6):
    _required_cpus = generate_random_values(1, 21, (number_slices, number_VNFs))
    return _required_cpus


def network_slicing(_number_VNFs, _number_slices, _total_number_centers, _required_cpus, _total_available_cpus):
    problem = pulp.LpProblem('Network_Slicing', pulp.LpMinimize)

    VNFs_placements = np.array([[[pulp.LpVariable(f'center_{k}_slice_{j}_VNF_{i}', cat=pulp.LpBinary)
                                  for k in range(_total_number_centers)]
                                 for i in range(_number_VNFs)]
                                for j in range(_number_slices)])

    # Maximization Problem
    problem += pulp.LpAffineExpression([(VNFs_placements[j, i, k], _required_cpus[j, i])
                                        for k in range(_total_number_centers)
                                        for i in range(_number_VNFs)
                                        for j in range(_number_slices)]), 'Objective'

    # Constraints
    constraint = 0

    # Constraint 1: CPU utilization does not exceed available CPU
    for k in range(_total_number_centers):
        problem += (pulp.LpAffineExpression([(VNFs_placements[j, i, k], _required_cpus[j, i])
                                            for i in range(_number_VNFs)
                                            for j in range(_number_slices)]) <= _total_available_cpus[k],
                    f'Constraint {constraint}')
        constraint += 1

    # Constraint 2: Each VNF is implemented once
    for i in range(_number_VNFs):
        for j in range(_number_slices):
            problem += (pulp.LpAffineExpression(
                [(VNFs_placements[j, i, k], 1) for k in range(_total_number_centers)]) <= 1, f'Constraint {constraint}')
            constraint += 1

    # Constraint 3: Either all VNFs of a slice is implemented or not
    binary_variables = [pulp.LpVariable(f'Slice_{j}_deployed', cat=pulp.LpBinary) for j in range(_number_slices)]
    for j in range(_number_slices):
        problem += (pulp.LpAffineExpression([(VNFs_placements[j, i, k], 1)
                                             for i in range(_number_VNFs)
                                             for k in range(_total_number_centers)])
                    == _number_VNFs * binary_variables[j],
                    f'Constraint {constraint}')
        constraint += 1

    # Solve
    problem.solve(pulp.PULP_CBC_CMD(msg=False))

    return np.vectorize(pulp.value)(VNFs_placements), np.vectorize(pulp.value)(binary_variables)


def main():
    # Define topology
    number_edge = 2
    number_cloud = 3
    total_number_centers, total_available_cpus = define_topology(number_edge=number_edge, number_cloud=number_cloud)

    # Define slices
    number_slices = 1
    number_VNFs = 6
    required_cpus = define_slices(number_slices=number_slices, number_VNFs=number_VNFs)

    # MILP
    solution, deployed_slices = network_slicing(number_VNFs, number_slices,
                                                total_number_centers, required_cpus, total_available_cpus)
    test_solution(solution, deployed_slices, required_cpus, total_available_cpus)


if __name__ == '__main__':
    main()
