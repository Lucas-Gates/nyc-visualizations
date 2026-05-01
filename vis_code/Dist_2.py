import matplotlib.pyplot as plt
import numpy as np
from vis_code.extra_funcs import *

def dist2(data):
    data_dist_2 = data.copy()

    hour_labels = [format_hour(h) for h in range(24)]

    # Aggregate: crash count by HOUR (all days combined)
    hourly = (data_dist_2.dropna(subset=['HOUR'])
        .groupby('HOUR')
        .size()
        .reset_index(name='CRASH_COUNT'))

    hours = np.arange(24)

    plt.figure(figsize=(11, 5))

    plt.bar(hours, hourly.set_index('HOUR')['CRASH_COUNT'].reindex(hours, fill_value=0),
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    # Shade rush hour bands
    plt.axvspan(7 - 0.5, 9 + 0.5, alpha=0.12, color='red', label='Rush Hours')
    plt.axvspan(16 - 0.5, 18 + 0.5, alpha=0.12, color='red')

    plt.title("NYC Motor Vehicle Crashes by Hour of Day")
    plt.xticks(hours, hour_labels, rotation=45)
    plt.xlabel("Time of Day")
    plt.ylabel("Total Crashes")
    plt.legend()
    plt.grid(alpha=0.3, linestyle='--')
    plt.xlim(-0.7, 23.7)
    plt.figtext(0.01, 0.02, "Shaded bands = morning (7–9 AM) and evening (4–6 PM) rush hours",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    plt.savefig('figures/fig2_distribution_crashes_by_hour.png')
    print("Figure saved as 'figures/fig2_distribution_crashes_by_hour.png'")

    plt.show()