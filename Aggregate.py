#--------------------------------------------#
# PART 3: Visualization — Crashes by Hour
#--------------------------------------------#

print("\n--------------------------------------------\n")
print("PART 3: Visualization — Crashes by Hour\n")
print("--------------------------------------------\n")

# Aggregate: crash count by HOUR and DAY_TYPE
hourly = (
    df_clean.dropna(subset=['HOUR'])
    .groupby(['HOUR', 'DAY_TYPE'])
    .size()
    .reset_index(name='CRASH_COUNT')
)

weekday = hourly[hourly['DAY_TYPE'] == 'Weekday'].set_index('HOUR')['CRASH_COUNT']
weekend = hourly[hourly['DAY_TYPE'] == 'Weekend'].set_index('HOUR')['CRASH_COUNT']

hours = np.arange(24)
bar_width = 0.4

plt.figure(figsize=(11, 5))

plt.bar(hours - bar_width / 2, weekday.reindex(hours, fill_value=0),
        width=bar_width, label='Weekday', color='teal', edgecolor='black', linewidth=1, alpha=0.85)
plt.bar(hours + bar_width / 2, weekend.reindex(hours, fill_value=0),
        width=bar_width, label='Weekend', color='orange', edgecolor='black', linewidth=1, alpha=0.85)

# Shade rush hour bands
plt.axvspan(7 - 0.5, 9 + 0.5, alpha=0.12, color='red', label='Rush Hours')
plt.axvspan(16 - 0.5, 18 + 0.5, alpha=0.12, color='red')

plt.title("NYC Motor Vehicle Crashes by Hour of Day\nWeekday vs. Weekend")
plt.xlabel("Hour of Day (0 = Midnight)")
plt.ylabel("Total Crashes")
plt.xticks(hours, [f'{h:02d}:00' for h in hours], rotation=45)
plt.legend()
plt.grid(alpha=0.3, linestyle='--')
plt.xlim(-0.7, 23.7)
plt.figtext(0.01, 0.02, "Shaded bands = morning (7–9 AM) and evening (4–6 PM) rush hours",
            fontsize=7, color='darkgray')

plt.tight_layout()

plt.savefig('fig1_crashes_by_hour.png')
print("Figure saved as 'fig1_crashes_by_hour.png'\n")

plt.show()
