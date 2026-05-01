import matplotlib.pyplot as plt

def agg(data):
    data_agg_1 = data.copy()

    # Aggregate: crash count by borough
    borough_counts = (
        data_agg_1['BOROUGH']
        .value_counts()
        .dropna()
        .reset_index()
    )
    borough_counts.columns = ['BOROUGH', 'CRASH_COUNT']

    plt.figure(figsize=(11, 5))

    plt.bar(borough_counts['BOROUGH'], borough_counts['CRASH_COUNT'],
            color='teal', edgecolor='black', linewidth=1, alpha=0.85)

    plt.title("NYC Motor Vehicle Crashes by Borough")
    plt.xlabel("Borough")
    plt.ylabel("Total Crashes")
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3, linestyle='--')
    plt.figtext(0.01, 0.02, "Based on borough recorded at time of crash report",
                fontsize=7, color='darkgray')

    plt.tight_layout()

    plt.savefig('figures/fig4_aggregate_crashes_by_borough.png')
    print("Figure saved as 'figures/fig4_aggregate_crashes_by_borough.png'")

    plt.show()