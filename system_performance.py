import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from utils import check_cpus_consumption


def system_performance(total_number_centers, total_available_cpus, assigned_cpus, VNFs_placements, alpha):
    fig, ax = plt.subplots()
    bar = None
    tab20 = plt.get_cmap('tab20')
    node_labels = [f"Node {i + 1}" for i in range(total_number_centers)]
    patterns = ['/', '\\', 'x', '|', 'o', 'O', '.', '*']

    consumed_cpus = VNFs_placements * assigned_cpus[:, :, np.newaxis]
    check_cpus_consumption(total_available_cpus, assigned_cpus, VNFs_placements)
    number_slices, number_VNFs, total_number_centers = consumed_cpus.shape
    bottom = np.zeros(total_number_centers)

    for s in range(number_slices):
        for k in range(number_VNFs):
            consumed_cpu = consumed_cpus[s, k, :]
            for c in range(total_number_centers):
                if consumed_cpu[c]:
                    consumed_cpu[c] = consumed_cpu[c] * 100 / total_available_cpus[c]
                ax.bar(node_labels, consumed_cpu, bottom=bottom, color=tab20(2 * s), hatch=patterns[k])

            bottom += consumed_cpu

    unused_cpu = 100 - bottom
    ax.bar(node_labels, unused_cpu, bottom=bottom, color='grey', label='Unused')
    ax.set_ylim([0, 110])
    ax.set_ylabel(f'CPU Usage (%)', fontsize=13)
    alpha_text = f'$\\alpha = {alpha}$'
    if alpha != 1:
        alpha_text = f'$\\alpha = {alpha:.2f}$'
    ax.set_title(f'CPU Utilization by Node | {alpha_text}', fontsize=17)

    color_patches = [Patch(facecolor=tab20(2 * i), label=f'Slice {i + 1}') for i in range(number_slices)]
    pattern_patches = [Patch(facecolor='white', edgecolor='black', hatch=patterns[i], label=f'VNF {i + 1}') for i in range(number_VNFs)]
    unused_patch = Patch(facecolor='grey', label='Unused CPU')

    # Combine all patches for the legend
    ax.legend(handles=[unused_patch] + color_patches + pattern_patches, bbox_to_anchor=(1.005, 1), loc='upper left')

    plt.show()
    pass

