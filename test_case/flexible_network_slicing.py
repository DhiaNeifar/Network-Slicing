import numpy as np
import pulp


def flexible_network_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                             total_available_bandwidth, edges_delay, number_VNFs, required_cpus, required_bandwidth,
                             delay_tolerance):

    problem = pulp.LpProblem('Flexible_Network_Slicing', pulp.LpMinimize)

    VNFs_placements = np.array([[[pulp.LpVariable(f'slice_{s}_center_{c}_VNF_{k}', cat=pulp.LpBinary)
                                  for c in range(total_number_centers)]
                                 for k in range(number_VNFs)]
                                for s in range(number_slices)])

    unassigned_cpus = np.array([[[pulp.LpVariable(f'unassigned_cpu_slice_{s}_center_{c}_VNF_{k}', cat=pulp.LpInteger,
                                                  lowBound=0)
                                  for c in range(total_number_centers)]
                                 for k in range(number_VNFs)]
                                for s in range(number_slices)])

    Virtual_links = np.array([[[[pulp.LpVariable(f'slice_{s}_VL{k}_to_VL{k + 1}_PN{i}_to_PN{j}', cat=pulp.LpBinary)
                                 for j in range(edges_adjacency_matrix.shape[1])]
                                for i in range(edges_adjacency_matrix.shape[0])]
                               for k in range(number_VNFs - 1)]
                              for s in range(number_slices)])


    missing_TP = np.array([[[[pulp.LpVariable(f'missing_TP_slice_{s}_VL{k}_to_VL{k + 1}_PN{i}_to_PN{j}',
                                              cat=pulp.LpInteger, lowBound=0)
                              for j in range(edges_adjacency_matrix.shape[1])]
                             for i in range(edges_adjacency_matrix.shape[0])]
                            for k in range(number_VNFs - 1)]
                           for s in range(number_slices)])

    '''
    Minimization Problem
    The following objective function focuses on minimizing the consumption of resources. If all constraints are met, 
    slices are deployed. Otherwise, the output would be None for all decision variables
    
    problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], required_cpus[s, k])
                                         for s in range(number_slices)
                                         for k in range(number_VNFs)
                                         for c in range(total_number_centers)]) +
                pulp.LpAffineExpression([(Virtual_links[s, k, i, j], required_bandwidth[s, k] + edges_delay[i, j])
                                         for s in range(number_slices)
                                         for k in range(number_VNFs - 1)
                                         for i in range(edges_adjacency_matrix.shape[0])
                                         for j in range(edges_adjacency_matrix.shape[1])]), 'Objective')
    
    '''

    '''
        Minimization Problem
        
        This objective function aims to minimize the total unmet CPU and ThroughPut requirements.
    
    '''

    problem += (pulp.LpAffineExpression([(unassigned_cpus[s, k, c], 1)
                                         for s in range(number_slices)
                                         for k in range(number_VNFs)
                                         for c in range(total_number_centers)]) +
                pulp.LpAffineExpression([(missing_TP[s, k, i, j], 1)
                                         for s in range(number_slices)
                                         for k in range(number_VNFs - 1)
                                         for i in range(edges_adjacency_matrix.shape[0])
                                         for j in range(edges_adjacency_matrix.shape[1])]), 'Objective')


    # Constraints
    constraint = 0

    # Node Embedding Constraints

    # Constraint 1: Each VNF is assigned only once to a center.
    for s in range(number_slices):
        for k in range(number_VNFs):
            problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1)
                                                 for c in range(total_number_centers)]) == 1,
                        f'constraint {constraint}')
            constraint += 1

    # Constraint 2: Each VNF is assigned to an exactly one center.
    for s in range(number_slices):
        for c in range(total_number_centers):
            problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1)
                                                 for k in range(number_VNFs)]) <= 1,
                        f'constraint {constraint}')
            constraint += 1

    # Constraint 3: Guarantee that allocated VNF resources do not exceed physical servers' processing capacity.
    for c in range(total_number_centers):
        problem += pulp.lpSum([(VNFs_placements[s, k, c] * required_cpus[s, k]) - unassigned_cpus[s, k, c]
                               for k in range(number_VNFs)
                               for s in range(number_slices)]) <= total_available_cpus[c], f'constraint {constraint}'
        constraint += 1

    # Constraint 4: Either all VNFs of a slice are implemented or not
    binary_variables = [pulp.LpVariable(f'Slice_{s}_deployed', cat=pulp.LpBinary)
                        for s in range(number_slices)]

    for s in range(number_slices):
        problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1) for k in range(number_VNFs) for c in
                                             range(total_number_centers)]) == number_VNFs * binary_variables[s],
                    f'Constraint {constraint}')
        constraint += 1

    # Link Embedding Constraints

    # Constraint 1: Flow Conservation Constraint
    for s in range(number_slices):
        for i in range(edges_adjacency_matrix.shape[0]):
            for k in range(number_VNFs - 1):
                problem += ((pulp.LpAffineExpression([(Virtual_links[s, k, i, j], edges_adjacency_matrix[i, j])
                                                      for j in range(edges_adjacency_matrix.shape[1])])) -
                            (pulp.LpAffineExpression([(Virtual_links[s, k, j, i], edges_adjacency_matrix[j, i])
                                                      for j in range(edges_adjacency_matrix.shape[1])])) ==
                            VNFs_placements[s, k, i] - VNFs_placements[s, k + 1, i], f'constraint {constraint}')
                constraint += 1

    # Constraint 2: Guarantee that allocated throughput resources do not exceed physical links' throughput capacity.

    for i in range(edges_adjacency_matrix.shape[0]):
        for j in range(edges_adjacency_matrix.shape[1]):
            problem += (pulp.lpSum([(Virtual_links[s, k, i, j] * required_bandwidth[s, k]) - missing_TP[s, k, i, j]
                                   for s in range(number_slices)
                                   for k in range(number_VNFs - 1)]) <= total_available_bandwidth[i, j],
                        f'constraint {constraint}')
            constraint += 1


    # Delay Tolerance Constraint
    # for s in range(number_slices):
    #     problem += (pulp.LpAffineExpression([(Virtual_links[s, k, i, j], edges_delay[i, j])
    #                                          for k in range(number_VNFs - 1)
    #                                          for i in range(edges_adjacency_matrix.shape[0])
    #                                          for j in range(edges_adjacency_matrix.shape[1])]) <= delay_tolerance[s],
    #                 f'constraint {constraint}')
    #     constraint += 1


    solver = pulp.CPLEX_CMD(path=r"C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\cplex\bin\x64_win64\cplex.exe")
    problem.solve(solver)
    return (np.vectorize(pulp.value)(VNFs_placements), np.vectorize(pulp.value)(Virtual_links),
            np.vectorize(pulp.value)(binary_variables), np.vectorize(pulp.value)(unassigned_cpus),
            np.vectorize(pulp.value)(missing_TP))


if __name__ == '__main__':
    pass
