import numpy as np
import networkx as nx


def simulate_attack(network):
    # Set alpha
    alpha = 0.5

    # Initialize all nodes as not failed
    failed_nodes = {node_: False for node_ in network.nodes()}

    # List to store failure times
    failure_times = {node_: 0.0 for node_ in network.nodes()}

    # Randomly choose an initial node to fail at time t
    initial_node = np.random.choice(network.nodes())
    initial_time = np.random.exponential(1 / 10)
    failed_nodes[initial_node] = True
    failure_times[initial_node] = initial_time

    # Nodes to be checked in the current iteration
    nodes_to_check = [initial_node]

    while nodes_to_check:
        new_nodes_to_check = []
        for node in nodes_to_check:
            for neighbor in network.neighbors(node):
                if not failed_nodes[neighbor]:
                    # Calculate time to fail for the neighbor
                    time_to_fail = failure_times[node] + np.random.exponential(1 / alpha)
                    failed_nodes[neighbor] = True
                    failure_times[neighbor] = time_to_fail
                    new_nodes_to_check.append(neighbor)
        nodes_to_check = new_nodes_to_check

    # Return the failure times for all nodes
    return failure_times


# Example usage
# Create a network (e.g., a simple star graph for demonstration)
network = nx.star_graph(n=5)  # Creates a star graph with 6 nodes (one center and 5 outer nodes)

# Simulate the attack
failure_times = simulate_attack(network)

# Print the failure times for each node
for node, time in failure_times.items():
    print(f"Node {node} failed at time {time:.4f}")
