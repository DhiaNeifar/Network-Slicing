import numpy as np
import pulp
from math import ceil


def slack_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                  total_available_bandwidth, edges_delay, number_VNFs, required_cpus, required_bandwidth,
                  delay_tolerance, failed_centers):


    problem = pulp.LpProblem('Slack_Slicing', pulp.LpMinimize)

    VNFs_placements = np.array([[[pulp.LpVariable(f'slice_{s}_center_{c}_VNF_{k}', cat=pulp.LpBinary)
                                  for c in range(total_number_centers)]
                                 for k in range(number_VNFs)]
                                for s in range(number_slices)])

    Virtual_links = np.array([[[[pulp.LpVariable(f'slice_{s}_VL{k}_to_VL{k + 1}_PN{i}_to_PN{j}', cat=pulp.LpBinary)
                                 for j in range(edges_adjacency_matrix.shape[1])]
                                for i in range(edges_adjacency_matrix.shape[0])]
                               for k in range(number_VNFs - 1)]
                              for s in range(number_slices)])

    slack_variables = np.array([pulp.LpVariable(f'slack_variable_center_{c}', cat=pulp.LpBinary)
                                for c in range(total_number_centers)])

    for failed_center in failed_centers:
        slack_variables[failed_center] = pulp.LpVariable(f'slack_variable_center_{failed_center}', lowBound=0,
                                                         upBound=0)
    # Objective Function

    problem += (pulp.LpAffineExpression([(slack_variables[c], 1)
                                         for c in range(total_number_centers)]) +
                pulp.LpAffineExpression([(Virtual_links[s, k, i, j], required_bandwidth[s, k])
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
                                                 for k in range(number_VNFs)]) <=
                        ceil(number_VNFs // max(1, (total_number_centers - len(failed_centers)))) + 1,
                        f'constraint {constraint}')
            constraint += 1

    # Constraint 3: Guarantee that allocated VNF resources do not exceed physical servers' processing capacity.
    for c in range(total_number_centers):
        problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], required_cpus[s, k])
                                             for s in range(number_slices)
                                             for k in range(number_VNFs)]) <=
                    total_available_cpus[c] + slack_variables[c], f'constraint {constraint}')
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
            problem += (pulp.LpAffineExpression([(Virtual_links[s, k, i, j], required_bandwidth[s, k])
                                                 for s in range(number_slices)
                                                 for k in range(number_VNFs - 1)]) <= total_available_bandwidth[i, j],
                        f'constraint {constraint}')
            constraint += 1

    problem.solve()
    return (np.vectorize(pulp.value)(VNFs_placements), np.vectorize(pulp.value)(Virtual_links),
            np.vectorize(pulp.value)(slack_variables))


if __name__ == '__main__':
    pass
