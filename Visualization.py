import numpy as np
import matplotlib.pyplot as plt


from graph_topology import graph_topology
from Timeline import timeline
from EpidemicModel import EpidemicModel
from EpidemicSpreadingSimulation import EpidemicSlicingSimulation


def Visualization():
    number_nodes = 50
    (total_number_centers, total_available_cpus, centers_task_execution_delay, edges_adjacency_matrix,
     total_available_bandwidth, edges_delay) = graph_topology(number_nodes)
    num_slices = 500
    arrival_times, departure_times = timeline(alpha=1.0, beta=0.01, num_slices=num_slices)

    gamma = 10.0
    initial_center, initial_time = (np.random.choice(total_number_centers),
                                    np.random.exponential(1 / gamma))

    spreads = [5, 1]
    for spread in spreads:
        centers, failure_times = EpidemicModel(total_number_centers, edges_adjacency_matrix, initial_center,
                                               spread=spread)
        system_performance, time_line, centers, failure_times = EpidemicSlicingSimulation(arrival_times,
                                                                                          departure_times,
                                                                                          centers, failure_times)
        plt.plot(time_line, system_performance, label=f'spread = {spread}')
    plt.legend()
    plt.show()

    pass



if __name__ == '__main__':
    Visualization()
