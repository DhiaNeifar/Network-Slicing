import numpy as np


def timeline(alpha=1.0, beta=0.01, num_slices=500):
    inter_arrival_times = np.random.exponential(1 / alpha, num_slices)
    arrival_times = np.cumsum(inter_arrival_times)
    durations = np.random.exponential(1 / beta, num_slices)
    departure_times = arrival_times + durations
    sorted_indices = np.argsort(departure_times)
    departure_times = np.array(departure_times)[sorted_indices]
    return arrival_times, departure_times
