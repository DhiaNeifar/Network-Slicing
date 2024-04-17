import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# Example data setup
number_nodes = 7
number_slices = 3
number_vnfs = 5

# Generate data
np.random.seed(0)  # Seed for reproducibility
required_cpus = np.random.randint(1, 5, (number_slices, number_vnfs))
VNFs_placement = np.zeros((number_slices, number_vnfs, number_nodes), dtype=int)
for s in range(number_slices):
    for v in range(number_vnfs):
        node = np.random.choice(number_nodes)
        VNFs_placement[s, v, node] = 1

total_available_cpus = np.random.randint(10, 20, number_nodes)

# CPU usage calculation
cpu_usage = np.zeros((number_nodes, number_slices * number_vnfs))
for node in range(number_nodes):
    for s in range(number_slices):
        for v in range(number_vnfs):
            if VNFs_placement[s, v, node] == 1:
                cpu_demand = required_cpus[s, v]
                # Prevent exceeding total available CPUs
                if np.sum(cpu_usage[node, :]) + cpu_demand > total_available_cpus[node]:
                    cpu_demand = total_available_cpus[node] - np.sum(cpu_usage[node, :])
                cpu_usage[node, s * number_vnfs + v] = cpu_demand

# Normalization
cpu_percentages = (cpu_usage.T / total_available_cpus).T * 100

# Plotting
fig, ax = plt.subplots()
base_colors = plt.cm.tab10(np.linspace(0, 1, number_slices))
patterns = [None, '/', '\\', '+', 'x', '-', '|', 'o', 'O', '.', '*']

node_labels = [f"Node {i+1}" for i in range(number_nodes)]
bottom = np.zeros(number_nodes)

for s in range(number_slices):
    for v in range(number_vnfs):
        i = s * number_vnfs + v
        color = to_rgba(base_colors[s], alpha=(1 - v / number_vnfs * 0.5))  # Gradually fade the color
        ax.bar(node_labels, cpu_percentages[:, i], bottom=bottom, color=color, hatch=patterns[v % len(patterns)],
               label=f'Slice {s} VNF {v}' if bottom.sum() == 0 else None)  # Label only first instance
        bottom += cpu_percentages[:, i]

# Unused CPU
unused_cpu = 100 - bottom
ax.bar(node_labels, unused_cpu, bottom=bottom, color='grey', label='Unused')

ax.set_ylabel('CPU Usage (%)')
ax.set_title('CPU Utilization by Node')

# Custom legend for patterns
handles, labels = ax.get_legend_handles_labels()
pattern_handles = [plt.Rectangle((0,0),1,1, fill=False, edgecolor='none', visible=False)] * len(patterns)
for i, pattern in enumerate(patterns):
    pattern_handles[i].set_hatch(pattern)
    pattern_handles[i].set_label(f'Pattern {i}')

ax.legend(handles=handles + pattern_handles, title="VNFs", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()
