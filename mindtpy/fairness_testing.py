import numpy as np
from scipy.optimize import minimize

# Given parameters
total_number_centers = 3
number_slices = 3
number_VNFs = 2
total_available_cpus = np.array([29, 18, 20], dtype=np.int16)
required_cpus = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)

# Flatten required_cpus for ease of use in vectorized operations
required_cpus_flat = required_cpus.flatten()


# Objective function to maximize fairness
def objective(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))

    sum_product = np.sum(
        [required_cpus[s, k] * VNFs_placements[s, k, c] for s in range(number_slices) for k in range(number_VNFs) for c
         in range(total_number_centers)])

    sum_squares = np.sum(
        [(required_cpus[s, k] * VNFs_placements[s, k, c]) ** 2 for s in range(number_slices) for k in range(number_VNFs)
         for c in range(total_number_centers)])

    fairness = ((1 / (number_slices * number_VNFs)) * sum_product ** 2) / sum_squares
    return -fairness  # Minimize negative to maximize fairness


# Constraints
constraints = []


# Constraint 1: Each VNF is assigned only once to a center.
def constraint_1_1(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))
    constraints_ = []
    for s in range(number_slices):
        for k in range(number_VNFs):
            constraints_.append(np.sum(VNFs_placements[s, k, :]) - 1e-4)
    return np.array(constraints_)


constraints.append({'type': 'ineq', 'fun': constraint_1_1})


def constraint_1_2(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))
    constraints_ = []
    for s in range(number_slices):
        for k in range(number_VNFs):
            for c in range(total_number_centers - 1):
                constraints_.append(VNFs_placements[s, k, c] * VNFs_placements[s, k, c + 1])
    return np.array(constraints_)


constraints.append({'type': 'eq', 'fun': constraint_1_2})


# # Constraint 2: Each VNF is assigned to an exactly one center.
def constraint_2_1(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))
    constraints_ = []
    for s in range(number_slices):
        for c in range(total_number_centers):
            constraints_.append(np.sum(VNFs_placements[s, :, c] - 1e-4))
    return np.array(constraints_)


constraints.append({'type': 'ineq', 'fun': constraint_2_1})


def constraint_2_2(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))
    constraints_ = []
    for s in range(number_slices):
        for c in range(total_number_centers):
            for k1 in range(number_VNFs - 1):
                for k2 in range(k1, number_VNFs):
                    constraints_.append(VNFs_placements[s, k1, c] * VNFs_placements[s, k2, c])
    return np.array(constraints_)


constraints.append({'type': 'eq', 'fun': constraint_2_2})


# CPU availability constraint
def constraint_cpu_availability(VNFs_placements_flat):
    VNFs_placements = VNFs_placements_flat.reshape((number_slices, number_VNFs, total_number_centers))
    cpu_constraints = []
    for c in range(total_number_centers):
        cpu_constraints.append(total_available_cpus[c] - np.sum([required_cpus[s, k] * VNFs_placements[s, k, c]
                                                                 for s in range(number_slices)
                                                                 for k in range(number_VNFs)]))
    return np.array(cpu_constraints)


constraints.append({'type': 'ineq', 'fun': constraint_cpu_availability})

# Initial guess (starting from a uniform distribution)
VNFs_placements_initial = np.random.uniform(0, 1, total_number_centers * number_slices * number_VNFs)

# Bounds for each variable in VNFs_placements
bounds = [(0, 1)] * (total_number_centers * number_slices * number_VNFs)

# Optimization
result = minimize(objective, VNFs_placements_initial, bounds=bounds, constraints=constraints, method='SLSQP')

print("'haze")
if result.success:
    # The result.x will give the continuous approximation of placements
    optimized_placements = result.x.reshape(number_slices, number_VNFs, total_number_centers)
    print("Optimization succeeded.")
    print("Optimized VNFs placements (continuous approximations):")
    print(optimized_placements)
else:
    print("Optimization failed:", result.message)
