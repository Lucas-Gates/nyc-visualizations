import matplotlib.pyplot as plt
import numpy as np
from vis_code.extra_funcs import format_hour
import webbrowser
import os

def dist2(data):

    # ── Data Preparation ────────────────────────────────────────────
    # Drop rows with no recorded hour, then count crashes per hour
    hourly = (
        data.dropna(subset=['HOUR'])
        .groupby('HOUR')
        .size()
        .reindex(np.arange(24), fill_value=0)
    )

    hours = np.arange(24)
    hour_labels = [format_hour(h) for h in hours]

    # ── Plot ─────────────────────────────────────────────────────────
    plt.figure(figsize=(11, 5))

    plt.bar(hours, hourly,
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    # Shade morning (7–9 AM) and evening (4–6 PM) rush hour bands
    for start, end in [(6.5, 9.5), (15.5, 18.5)]:
        plt.axvspan(start, end, alpha=0.12, color='red')
    plt.axvspan(0, 0, alpha=0.12, color='red', label='Rush Hours')  # Dummy for legend

    # ── Labels & Formatting ──────────────────────────────────────────
    plt.title("NYC Motor Vehicle Crashes by Hour of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Total Crashes")
    plt.xticks(hours, hour_labels, rotation=45)
    plt.xlim(-0.7, 23.7)
    plt.legend()
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "Shaded bands = morning (7–9 AM) and evening (4–6 PM) rush hours",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    # ── Export ───────────────────────────────────────────────────────
    plt.savefig('figures/fig2_distribution_crashes_by_hour.png')
    print("Figure saved as 'figures/fig2_distribution_crashes_by_hour.png'")

    webbrowser.open("file://" + os.path.abspath("figures/fig2_distribution_crashes_by_hour.png"))
