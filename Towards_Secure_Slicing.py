import numpy as np
import pulp


def generate_random_values(low, high, size, _type='int'):
    if _type == 'int':
        return np.random.randint(low=low, high=high, size=size, dtype=np.int16)
    return np.random.uniform(low=low, high=high, size=size)


def define_physical_links(_total_number_centers, _links):
    _physical_links_bandwidth = np.zeros((_total_number_centers, _total_number_centers), dtype=np.int16)
    _physical_links_delay = np.zeros((_total_number_centers, _total_number_centers), dtype=np.float16)
    for _link in _links:
        bandwidth = generate_random_values(low=100, high=201, size=1, _type='int')[0]
        delay = generate_random_values(low=0.25, high=0.76, size=1, _type='float')[0]
        _physical_links_bandwidth[_link[0], _link[1]] = bandwidth
        _physical_links_bandwidth[_link[1], _link[0]] = bandwidth
        _physical_links_delay[_link[0], _link[1]] = delay
        _physical_links_delay[_link[1], _link[0]] = delay
    return _physical_links_bandwidth, _physical_links_delay


def define_topology(number_edge=2, number_cloud=3):
    _number_edge = number_edge
    _number_cloud = number_cloud
    _total_number_centers = _number_cloud + _number_edge
    available_edge_cpus = generate_random_values(10, 41, number_edge)
    available_cloud_cpus = generate_random_values(20, 201, number_cloud)
    links = [[0, 3], [3, 2], [3, 4], [2, 4], [1, 4]]
    physical_links_bandwidth, physical_links_delay = define_physical_links(_total_number_centers, links)
    _total_available_cpus = np.concatenate((available_edge_cpus, available_cloud_cpus), axis=0, dtype=np.int16)
    return _total_number_centers, _total_available_cpus, physical_links_bandwidth, physical_links_delay


def slice_requirements(_number_VNFs):
    _E2E_delay = generate_random_values(1, 11, 1)
    _required_cpus = generate_random_values(1, 21, _number_VNFs)
    _required_bandwidth_per_VNF = generate_random_values(10, 31, _number_VNFs - 1)
    _required_bandwidth = np.zeros((_number_VNFs, _number_VNFs))
    _required_bandwidth[1:, 0] = _required_bandwidth_per_VNF
    _required_bandwidth[0, 1:] = _required_bandwidth_per_VNF
    return _E2E_delay, _required_cpus, _required_bandwidth


def network_slicing(_number_VNFs, _total_number_centers, _E2E_delay, _required_cpus, _required_bandwidth,
                    _total_available_cpus, _physical_links_bandwidth, _physical_links_delay):

    _total_used_cpus = np.zeros(_total_available_cpus.shape)
    _total_used_bandwidth = np.zeros(_physical_links_bandwidth.shape)

    problem = pulp.LpProblem('Network_Slicing', pulp.LpMinimize)

    VNFs_placements = np.array(
        [[pulp.LpVariable(f'center_{k}_VNF_{i}', cat=pulp.LpBinary) for k in range(_total_number_centers)] for i in
         range(_number_VNFs)])

    Virtual_links = np.array([[
        [[pulp.LpVariable(f'VL{i}{j}_PL{e}_PL{f}', lowBound=0) for e in range(_physical_links_delay.shape[0])] for f
         in range(_physical_links_delay.shape[1])] for i in range(_number_VNFs)] for j in range(_number_VNFs)])
    print(Virtual_links.shape)

    # Minimization Problem
    problem += (pulp.LpAffineExpression(
        [(VNFs_placements[i, k], _total_used_cpus[k] + _required_cpus[i]) for k in range(_total_number_centers) for
         i in range(_number_VNFs)]) + pulp.LpAffineExpression(
        [(Virtual_links[i, j, e, f], _physical_links_delay[e, f]) for i in range(_number_VNFs) for j in range(_number_VNFs) for e in
         range(_physical_links_delay.shape[0]) for f in range(_physical_links_delay.shape[1]) if e != f]), 'Objective')

    # Constraints

    # Constraint 1: Each VNF is assigned to an exactly one server.
    constraint = 0
    for i in range(_number_VNFs):
        problem += pulp.LpAffineExpression([(VNFs_placements[i, k], 1) for k in range(_total_number_centers)]) == 1, f'constraint {constraint}'
        constraint += 1

    # Constraint 2: Guarantee that that allocated VNF resources do not exceed physical servers' processing capacity.
    for k in range(_total_number_centers):
        problem += pulp.LpAffineExpression(
            [(VNFs_placements[i, k], _total_used_cpus[k] + _required_cpus[i]) for i in range(_number_VNFs)]) <= \
                   _total_available_cpus[k], f'constraint {constraint}'
        constraint += 1

    # Constraint 3: Guarantee that that allocated VNF resources do not exceed physical links' bandwidth.
    for i in range(_number_VNFs):
        for j in range(_number_VNFs):
            problem += pulp.LpAffineExpression([(Virtual_links[i, j, e, f], _total_used_bandwidth[e, f] + _required_bandwidth[i, j]) for e in range(_physical_links_delay.shape[0]) for f in range(_physical_links_delay.shape[1])]) <= _physical_links_bandwidth[i], f'constraint {constraint}'
            constraint += 1

    # Constraint 4: Ensure that partial allocation of a slice is not the desired behavior. Doesn't Work! for i in
    # range(_number_VNFs): for k in range(_total_number_centers): problem += _required_cpus[i] <= (
    # _total_available_cpus[k] - _total_used_cpus[k]), 'constraint {constraint}' constraint += 1

    # Constraint 5: The conservation of flows; The sum of all incoming and outgoing traffic in the physical nodes
    # that do not host VNFs should be zero.
    for i in range(_number_VNFs):
        for j in range(_number_VNFs):
            for e in range(_physical_links_delay.shape[0]):
                for f in range(_physical_links_delay.shape[1]):
                    problem += Virtual_links[i, j, e, f] - Virtual_links[i, j, f, e] == VNFs_placements[i, e] - VNFs_placements[j, e]
                    constraint += 1
    problem.solve()
    return 0, 1


def Simulation():
    # Define topology
    number_edge = 2
    number_cloud = 3
    total_number_centers, total_available_cpus, physical_links_bandwidth, physical_links_delay = define_topology(
        number_edge=number_edge, number_cloud=number_cloud)

    number_VNFs = 4
    E2E_delay, required_cpus, required_bandwidth = slice_requirements(number_VNFs)
    # MILP
    solution, deployed_slices = network_slicing(number_VNFs, total_number_centers, E2E_delay, required_cpus,
                                                required_bandwidth, total_available_cpus, physical_links_bandwidth,
                                                physical_links_delay)


if __name__ == "__main__":
    Simulation()
