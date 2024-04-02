import pulp
import numpy as np



total_number_centers = 3
total_available_cpus = np.array([29, 18, 20], dtype=np.int16)

number_slices = 3
number_VNFs = 2
required_cpus = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)


problem = pulp.LpProblem('Flexible_Network_Slicing', pulp.LpMaximize)

VNFs_placements = np.array([[[pulp.LpVariable(f'slice_{s}_center_{c}_VNF_{k}', cat=pulp.LpBinary) for c in
                              range(total_number_centers)] for k in range(number_VNFs)] for s in range(number_slices)])


problem += (pulp.LpAffineExpression(
    [(VNFs_placements[s, k, c], required_cpus[s, k]) for s in range(number_slices) for k in range(number_VNFs) for c in
     range(total_number_centers)]), 'Objective')


# Constraints
constraint = 0

# Node Embedding Constraints

# Constraint 1: Each VNF is assigned only once to a center.
for s in range(number_slices):
    for k in range(number_VNFs):
        problem += (
            pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1) for c in range(total_number_centers)]) == 1,
            f'constraint {constraint}')
        constraint += 1

# Constraint 2: Each VNF is assigned to an exactly one center.
for s in range(number_slices):
    for c in range(total_number_centers):
        problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], 1) for k in range(number_VNFs)])
                    <= 1,
                    f'constraint {constraint}')
        constraint += 1

# Constraint 3: Guarantee that allocated VNF resources do not exceed physical servers' processing capacity.
for c in range(total_number_centers):
    problem += (pulp.LpAffineExpression([(VNFs_placements[s, k, c], required_cpus[s, k])
                                         for k in range(number_VNFs)
                                         for s in range(number_slices)]) <= total_available_cpus[c],
                f'constraint {constraint}')
    constraint += 1

problem.solve()

print(np.vectorize(pulp.value)(VNFs_placements))


