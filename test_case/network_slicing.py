import numpy as np
import pulp


def network_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                    total_available_bandwidth, number_VNFs, required_cpus, required_bandwidth):
    problem = pulp.LpProblem('Network_Slicing', pulp.LpMinimize)

    VNFs_placements = np.array([[[pulp.LpVariable(f'slice_{s}_center_{c}_VNF_{k}', cat=pulp.LpBinary)
                                  for c in range(total_number_centers)]
                                 for k in range(number_VNFs)]
                                for s in range(number_slices)])

    Virtual_links = np.array([[[[pulp.LpVariable(f'slice_{s}_VL{k}_to_VL{k + 1}_PN{i}_to_PN{j}', cat=pulp.LpBinary)
                                 for j in range(edges_adjacency_matrix.shape[1])]
                                for i in range(edges_adjacency_matrix.shape[0])]
                               for k in range(number_VNFs - 1)]
                              for s in range(number_slices)])

    # Minimization Problem
    problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], required_cpus[s, k])
                                         for s in range(number_slices)
                                         for k in range(number_VNFs)
                                         for c in range(total_number_centers)]), 'Objective')

    # # + pulp.LpAffineExpression([(Virtual_links[s, t, i, j], edges_delay[i, j])
    # #                                      for s in range(edges_adjacency_matrix.shape[0])
    # #                                      for t in range(edges_adjacency_matrix.shape[1])
    # #                                      for i in range(edges_adjacency_matrix.shape[0])
    # #                                      for j in range(edges_adjacency_matrix.shape[1])]), 'Objective')

    # Constraints
    constraint = 0

    # Node Embedding Constraints

    # Constraint 1: Each VNF is assigned to an exactly one center.
    for s in range(number_slices):
        for c in range(total_number_centers):
            problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1)
                                                 for k in range(number_VNFs)]) <= number_VNFs,
                        f'constraint {constraint}')
            constraint += 1

    # Constraint 2: Each VNF is assigned only once to a center.
    for s in range(number_slices):
        for k in range(number_VNFs):
            problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1)
                                                 for c in range(total_number_centers)]) == 1,
                        f'constraint {constraint}')
            constraint += 1

    # Constraint 3: Guarantee that allocated VNF resources do not exceed physical servers' processing capacity.
    for c in range(total_number_centers):
        problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], required_cpus[s, k])
                                             for k in range(number_VNFs)
                                             for s in range(number_slices)]) <= total_available_cpus[c],
                    f'constraint {constraint}')
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

    # # Constraint 4.1: Avoid loops while embedding a virtual link
    # # for c in range(total_number_centers):
    #
    # Solve
    # problem.solve()
    solver = pulp.CPLEX_CMD(path=r"C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\cplex\bin\x64_win64\cplex.exe")
    problem.solve(solver)
    return (np.vectorize(pulp.value)(VNFs_placements), np.vectorize(pulp.value)(Virtual_links),
            np.vectorize(pulp.value)(binary_variables))


if __name__ == '__main__':
    pass
