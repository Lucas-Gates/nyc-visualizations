import matplotlib.pyplot as plt
import webbrowser
import os

# ── Constants ────────────────────────────────────────────────────────────────

BOROUGH_POPULATION = {
    'Brooklyn'     : 2_736_074,
    'Queens'       : 2_405_464,
    'Manhattan'    : 1_694_251,
    'Bronx'        : 1_472_654,
    'Staten Island':   495_747,
}

def agg(data):
    """
    Aggregation visualization: Total crash count by NYC borough.
    Produces two figures — raw counts and population-normalized counts.
    """

    # ── Data Preparation ────────────────────────────────────────────
    # Count crashes per borough, drop missing, sort descending
    borough_counts = (
        data['BOROUGH']
        .value_counts()
        .dropna()
        .rename_axis('BOROUGH')
        .reset_index(name='CRASH_COUNT')
    )

    # Normalize by population — crashes per 100,000 residents
    borough_counts['POPULATION'] = borough_counts['BOROUGH'].map(BOROUGH_POPULATION)
    borough_counts['CRASHES_PER_100K'] = (
        borough_counts['CRASH_COUNT'] / borough_counts['POPULATION'] * 100_000
    ).round(1)

    # ── Figure 1: Raw Crash Counts ───────────────────────────────────
    plt.figure(figsize=(11, 5))

    plt.bar(borough_counts['BOROUGH'], borough_counts['CRASH_COUNT'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    plt.title("NYC Motor Vehicle Crashes by Borough\nRaw Count")
    plt.xlabel("Borough")
    plt.ylabel("Total Crashes")
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "Based on borough recorded at time of crash report",
                fontsize=7, color='darkgray')

    plt.tight_layout()
    
    plt.savefig('figures/fig4a_aggregate_crashes_by_borough.png')
    print("Figure saved as 'figures/fig4a_aggregate_crashes_by_borough.png'")

    webbrowser.open("file://" + os.path.abspath("figures/fig4a_aggregate_crashes_by_borough.png"))

    # ── Figure 2: Normalized by Population ──────────────────────────
    plt.figure(figsize=(11, 5))

    plt.bar(borough_counts['BOROUGH'], borough_counts['CRASHES_PER_100K'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    plt.title("NYC Motor Vehicle Crashes by Borough\nPer 100,000 Residents")
    plt.xlabel("Borough")
    plt.ylabel("Crashes per 100,000 Residents")
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "Normalized by 2020 Census population. Source: Wikipedia — Boroughs of New York City.",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    plt.savefig('figures/fig4b_aggregate_crashes_by_borough_normalized.png')
    print("Figure saved as 'figures/fig4b_aggregate_crashes_by_borough_normalized.png'")

    webbrowser.open("file://" + os.path.abspath("figures/fig4b_aggregate_crashes_by_borough_normalized.png"))