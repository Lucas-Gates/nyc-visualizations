import matplotlib.pyplot as plt
import webbrowser
import os

def agg(data):

    # ── Data Preparation ────────────────────────────────────────────
    # Count crashes per borough, drop missing, sort descending
    borough_counts = (
        data['BOROUGH']
        .value_counts()
        .dropna()
        .rename_axis('BOROUGH')
        .reset_index(name='CRASH_COUNT')
    )

    # ── Plot ─────────────────────────────────────────────────────────
    plt.figure(figsize=(11, 5))

    plt.bar(borough_counts['BOROUGH'], borough_counts['CRASH_COUNT'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    # ── Labels & Formatting ──────────────────────────────────────────
    plt.title("NYC Motor Vehicle Crashes by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Total Crashes")
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "Based on borough recorded at time of crash report",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    # ── Export ───────────────────────────────────────────────────────
    plt.savefig('figures/fig4_aggregate_crashes_by_borough.png')
    print("Figure saved as 'figures/fig4_aggregate_crashes_by_borough.png'")

    webbrowser.open("file://" + os.path.abspath("figures/fig4_aggregate_crashes_by_borough.png"))
