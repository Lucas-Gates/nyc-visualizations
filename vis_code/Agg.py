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
    Produces two figures — raw counts (all years) and population-normalized
    counts (2020 only, matched to Census population data).
    """

    # ── Data Preparation: Raw (All Years) ───────────────────────────
    borough_counts = (
        data['BOROUGH']
        .value_counts()
        .dropna()
        .rename_axis('BOROUGH')
        .reset_index(name='CRASH_COUNT')
    )

    # ── Data Preparation: Normalized (2021 Only) ─────────────────────
    # Filter to 2021 to match the Census population data
    borough_2021 = (
        data[data['YEAR'] == 2021]['BOROUGH']
        .value_counts()
        .dropna()
        .rename_axis('BOROUGH')
        .reset_index(name='CRASH_COUNT')
    )

    borough_2021['POPULATION'] = borough_2021['BOROUGH'].map(BOROUGH_POPULATION)
    borough_2021['CRASHES_PER_100K'] = (
        borough_2021['CRASH_COUNT'] / borough_2021['POPULATION'] * 100_000
    ).round(1)

    # ── Figure 1: Raw Crash Counts (All Years) ───────────────────────
    plt.figure(figsize=(11, 5))

    plt.bar(borough_counts['BOROUGH'], borough_counts['CRASH_COUNT'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    plt.title("NYC Motor Vehicle Crashes by Borough\nAll Years")
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

    # ── Figure 2: Normalized by Population (2021 Only) ───────────────
    plt.figure(figsize=(11, 5))

    plt.bar(borough_2021['BOROUGH'], borough_2021['CRASHES_PER_100K'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    plt.title("NYC Motor Vehicle Crashes by Borough\nPer 100,000 Residents (2021)")
    plt.xlabel("Borough")
    plt.ylabel("Crashes per 100,000 Residents")
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "2021 crash data normalized by 2021 U.S. Census population. Source: Wikipedia — Boroughs of New York City.",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    plt.savefig('figures/fig4b_aggregate_crashes_by_borough_normalized.png')
    print("Figure saved as 'figures/fig4b_aggregate_crashes_by_borough_normalized.png'")

    webbrowser.open("file://" + os.path.abspath("figures/fig4b_aggregate_crashes_by_borough_normalized.png"))