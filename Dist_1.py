import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#12 hour labels
def format_hour(h):
    if h == 0:
        return "12 AM"
    elif h < 12:
        return f"{h} AM"
    elif h == 12:
        return "12 PM"
    else:
        return f"{h - 12} PM"
    
def dist1(data):
    data_dist_1 = data.copy()

    hour_labels = [format_hour(h) for h in range(24)]

    #plot
    plt.figure(figsize=(11, 5))
    colors = {
        "Property Damage": "blue",
        "Injury": "orange",
        "Fatal": "red"
    }
    plot_order = ["Property Damage", "Injury", "Fatal"]
    for severity in plot_order:
        subset = data_dist_1[data_dist_1["SEVERITY_LABEL"] == severity]
        counts = subset["HOUR"].value_counts().sort_index()
        counts = counts.reindex(range(24), fill_value=0)
        percent = counts / counts.sum() * 100
        smooth = percent.rolling(window=3, center=True, min_periods=1).mean()
        plt.fill_between(range(24), smooth, alpha=0.15, color=colors[severity])
        plt.plot(range(24), smooth, label=severity, color=colors[severity], linewidth=2)

    #axis formatting
    plt.xticks(range(24), hour_labels, rotation=45)
    plt.xlim(0, 23)
    plt.margins(x=0)

    #labels and legend
    plt.title("Crashes by Percent by Hour and Severity")
    plt.xlabel("Time of Day")
    plt.ylabel("Percent of Crashes")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend(title="Crash Severity")

    #save and show
    plt.tight_layout()
    plt.savefig("fig1_distribution_danger_window.png")
    print("Figure saved as 'fig1_distribution_danger_window.png'\n")
    plt.show()