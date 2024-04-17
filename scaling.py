import numpy as np
import pulp


from fairness_slicing import fairness_slicing


def scaling(status, parameters):
    solution = None
    parameters[7] = np.copy(parameters[7]).astype(np.float32)
    required_cpus_decimals = parameters[7] / 10
    required_cpus_units = parameters[7] / 100
    alpha = 1
    while status == pulp.LpStatusInfeasible:
        print("Solution not solved.")
        parameters[7] -= required_cpus_decimals
        alpha -= 0.1
        status, solution = fairness_slicing(*parameters)

    parameters[7] += required_cpus_units

    status_, solution_ = fairness_slicing(*parameters)
    while status_ == pulp.LpStatusOptimal:
        status, solution = status_, solution_
        alpha += 0.01
        status_, solution_ = fairness_slicing(*parameters)

    return status, solution, alpha
