import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import geopandas as gpd
import plotly.express as px


#------#
# START
#------#

print("\n\n--------------------------\n")
print("CS_2300 - Final Project\n")
print("--------------------------\n\n")


#--------------------------------#
# PART 1: Load & Inspect Raw Data
#--------------------------------#

print("--------------------------------\n")
print("PART 1: Load & Inspect Raw Data\n")
print("--------------------------------\n")

df = pd.read_csv(r'Data\Motor_Vehicle_Collisions_-_Crashes_20260421.csv', low_memory=False)

# First 5 rows
print("First 5 Rows: \n")
print(df.head(), "\n")

# Number of rows & columns
print(f"Total Number of Rows: {df.shape[0]}\nTotal Number of Columns: {df.shape[1]} \n")

# Column names
print("Column Names: ", df.columns, "\n")

# Data types
print("Data Types:\n", df.dtypes.to_string(), "\n")

# Check for missing values
miss_val = df.isna().sum()

if miss_val.sum() >= 1:
    print("\n!!! MISSING DATA DETECTED !!!\n")
    print("Missing Values: \n", (miss_val.to_string()), "\n")
else:
    print("*** No missing data ***\n")
    print("Missing Values: \n", (miss_val.to_string()), "\n")

# Identify duplicate rows
df_dups = df[df.duplicated()]
dups = df_dups.shape[0]

if dups >= 1:
    print("\n!!! DUPLICATE DATA DETECTED !!!\n")
    print(f"Total Number of Duplicate Rows: {dups}\n")
else:
    print("\n*** No duplicate data detected ***\n\n")


#----------------------------#
# PART 2: Basic Data Cleaning
#----------------------------#

print("\n----------------------------\n")
print("PART 2: Basic Data Cleaning\n")
print("----------------------------\n")

df_clean = df.copy()

# Standardize column names (strip spaces, uppercase, underscores)
df_clean.columns = df_clean.columns.str.strip().str.upper().str.replace(r'\s+', '_', regex=True)
print("Column names standardized.\n")

# Drop duplicate rows
before = len(df_clean)
df_clean = df_clean.drop_duplicates()
print(f"Duplicate rows removed              : {before - len(df_clean):,}")

# Drop rows missing both location AND borough (not usable for geo work)
before = len(df_clean)
df_clean = df_clean.dropna(subset=['LATITUDE', 'LONGITUDE', 'BOROUGH'], how='all')
print(f"Rows dropped (no location/borough)  : {before - len(df_clean):,}")

# Parse CRASH DATE and extract all time features together
df_clean['CRASH_DATE'] = pd.to_datetime(df_clean['CRASH_DATE'], errors='coerce')
df_clean['HOUR']        = pd.to_datetime(df_clean['CRASH_TIME'], format='%H:%M', errors='coerce').dt.hour
df_clean['DAY_OF_WEEK'] = df_clean['CRASH_DATE'].dt.dayofweek       # numeric — needed for DAY_TYPE
df_clean['DAY_TYPE']    = df_clean['DAY_OF_WEEK'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
df_clean['DAY_OF_WEEK'] = df_clean['CRASH_DATE'].dt.day_name()      # now safe to overwrite with names
df_clean['MONTH']       = df_clean['CRASH_DATE'].dt.month
df_clean['YEAR']        = df_clean['CRASH_DATE'].dt.year

unparseable = df_clean['CRASH_DATE'].isna().sum()
print(f"Unparseable dates                   : {unparseable:,}")

# Fix ZIP CODE to be a string, never a number
df_clean['ZIP_CODE'] = df_clean['ZIP_CODE'].astype(str).str.zfill(5).str.strip()
df_clean['ZIP_CODE'] = df_clean['ZIP_CODE'].replace({'nan': np.nan, '00000': np.nan})
print(f"ZIP_CODE cleaned and standardized.\n")

# Standardize BOROUGH title case, unknown → NaN
df_clean['BOROUGH'] = df_clean['BOROUGH'].str.strip().str.title()
valid_boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
df_clean.loc[~df_clean['BOROUGH'].isin(valid_boroughs), 'BOROUGH'] = np.nan
print(f"BOROUGH standardized. Invalid entries set to NaN.\n")

# Standardize contributing factors: blank/unspecified → NaN
unspecified = ['Unspecified', '1', '', 'nan']
for col in ['CONTRIBUTING_FACTOR_VEHICLE_1', 'CONTRIBUTING_FACTOR_VEHICLE_2']:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].str.strip().str.title()
        df_clean[col] = df_clean[col].replace(unspecified, np.nan)

# Standardize vehicle type codes: consolidate common variants
vehicle_map = {
    'Sedan'      : ['Sedan', '4 Dr Sedan', '2 Dr Sedan', 'Passenger Vehicle'],
    'SUV'        : ['Station Wagon/Sport Utility Vehicle', 'Suv'],
    'Taxi'       : ['Taxi', 'Taxi Cab'],
    'Bus'        : ['Bus', 'Omnibus', 'School Bus'],
    'Truck'      : ['Truck', 'Pick-Up Truck', 'Box Truck', 'Flat Bed'],
    'Motorcycle' : ['Motorcycle', 'Motorbike'],
    'Bicycle'    : ['Bike', 'Bicycle', 'E-Bike'],
}
lookup = {v.lower(): k for k, variants in vehicle_map.items() for v in variants}

if 'VEHICLE_TYPE_CODE_1' in df_clean.columns:
    df_clean['VEHICLE_TYPE_CODE_1'] = (
        df_clean['VEHICLE_TYPE_CODE_1']
        .str.strip().str.title()
        .map(lambda x: lookup.get(str(x).lower(), x) if pd.notna(x) else np.nan)
    )

# Create SEVERITY column
# 0 = property damage only, 1 = injury, 2 = fatality
def assign_severity(row):
    if row.get('NUMBER_OF_PERSONS_KILLED', 0) > 0:
        return 2
    elif row.get('NUMBER_OF_PERSONS_INJURED', 0) > 0:
        return 1
    else:
        return 0

df_clean['SEVERITY'] = df_clean.apply(assign_severity, axis=1)
severity_labels = {0: 'Property Damage', 1: 'Injury', 2: 'Fatal'}
df_clean['SEVERITY_LABEL'] = df_clean['SEVERITY'].map(severity_labels)

# Summary after cleaning
print(f"\nRows remaining after cleaning: {len(df_clean):,}")
print(f"\nSeverity Distribution:")
print(df_clean['SEVERITY_LABEL'].value_counts().to_string())
print(f"\nBorough Distribution (after cleaning):")
print(df_clean['BOROUGH'].value_counts(dropna=False).to_string())
print(f"\nYear Range: {df_clean['YEAR'].min()} – {df_clean['YEAR'].max()}")
print("\n[INFO] Basic cleaning complete.\n")

#save cleaned dataset
output_path = r'data\cleaned_motor_vehicle_crashes.csv'
df_clean.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to: {output_path}\n")


#-------------------------------------------------#
# PART 3: Distribution Visualization - Crash Severity by Hour
#-------------------------------------------------#

print("\n-------------------------------------------------\n")
print("PART 3: Distribution Visualization - Crash Severity By Hour\n")
print("-------------------------------------------------\n")

data_3 = df_clean.copy()

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
    subset = data_3[data_3["SEVERITY_LABEL"] == severity]
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


#-------------------------------------------------#
# PART 4: Distribution Visualization - Total Crashes By Hour
#-------------------------------------------------#

print("\n-------------------------------------------------\n")
print("PART 4: Distribution Visualization - Total Crashes By Hour\n")
print("-------------------------------------------------\n")

data5 = df_clean.copy()

# Aggregate: crash count by HOUR (all days combined)
hourly = (data5.dropna(subset=['HOUR'])
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
plt.xlabel("Hour of Day (0 = Midnight)")
plt.ylabel("Total Crashes")
plt.xticks(hours, [f'{h:02d}:00' for h in hours], rotation=45)
plt.legend()
plt.grid(alpha=0.3, linestyle='--')
plt.xlim(-0.7, 23.7)
plt.figtext(0.01, 0.02, "Shaded bands = morning (7–9 AM) and evening (4–6 PM) rush hours",
            fontsize=7, color='darkgray')

plt.tight_layout()

plt.savefig('fig2_distribution_crashes_by_hour.png')
print("Figure saved as 'fig2_distribution_crashes_by_hour.png'\n")

plt.show()


#-------------------------------------------------#
# PART 5: Relationship Visualization - Crashes by Hour
#-------------------------------------------------#

print("\n-------------------------------------------------\n")
print("PART 5: Relationship Visualization — Crashes by Hour\n")
print("-------------------------------------------------\n")

data4 = df_clean.copy()

###data = data[::5]


data4 = data4[data4['LATITUDE'].notna() & data4['LONGITUDE'].notna()]
data4 = data4.drop(columns = ['ZIP_CODE'])
data4 = data4[data4['NUMBER_OF_PERSONS_INJURED'].notna() & data4['NUMBER_OF_PERSONS_KILLED'].notna()]

data4['CRASH_DATE'] = pd.to_datetime(data4['CRASH_DATE'])


data4['YEAR'] = data4['CRASH_DATE'].dt.year

data4 = data4[data4['YEAR'] != 2026]
years = data4.groupby('YEAR').agg(
    CRASH_COUNT=('COLLISION_ID', 'size'),
    TOTAL_INJURED=('NUMBER_OF_PERSONS_INJURED', 'sum'),
    AVG_INJURED=('NUMBER_OF_PERSONS_INJURED', 'mean')
).reset_index()

min_s, max_s = 10, 60  # control your min/max dot size

years['SIZES'] = (years['AVG_INJURED'] - years['AVG_INJURED'].min()) / \
        (years['AVG_INJURED'].max() - years['AVG_INJURED'].min()) \
        * (max_s - min_s) + min_s


fig = px.scatter(years, x='YEAR', y='CRASH_COUNT', size='AVG_INJURED', 
                 hover_data=['YEAR', 'CRASH_COUNT', 'AVG_INJURED'],
                 labels ={'YEAR': 'Year', 'CRASH_COUNT': 'Number of Crashes', 'AVG_INJURED': 'Average_Injuries_per_Incident'},title = 'NYC\'s Decline in Crashes, Increase in Danger ',  size_max= 120)

fig.write_html("fig3_crashDanger.html")

fig.show()


#----#
# END
#----#

print("\n\n---------------\n")
print("END OF PROGRAM\n")
print("---------------\n\n")