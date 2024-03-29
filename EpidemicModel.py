import numpy as np


def EpidemicModel(total_number_centers, edges_adjacency_matrix, spread=0.5):
    total_number_centers -= 1
    edges_adjacency_matrix = edges_adjacency_matrix[:-1, :-1]
    initial_center = np.random.choice(total_number_centers)
    failed_centers = [0 for _ in range(total_number_centers)]
    failed_centers[initial_center] = 1
    Rounds = [[], [initial_center]]
    while sum(failed_centers) != len(failed_centers):
        Round = []
        for center, state in enumerate(failed_centers):
            if state:
                for neighbor in range(total_number_centers):
                    if (neighbor != center and edges_adjacency_matrix[center, neighbor] and not failed_centers[neighbor]
                            and np.random.uniform(0, 1) < spread):
                        Round.append(neighbor)
                        failed_centers[neighbor] = 1
        Rounds.append(Round)
    return Rounds
