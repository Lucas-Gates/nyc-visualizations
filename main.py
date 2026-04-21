import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#------#
# START
#------#

print("\n\n--------------------------\n")
print("CS_2300 - Final Project\n")
print("--------------------------\n\n")


#--------------------------------#
# PART 1: Load & Inspect Raw Data
#--------------------------------#

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


#----------------------------#
# PART 2: Basic Data Cleaning
#----------------------------#

# Standardize column names (strip spaces, uppercase, underscores)
df.columns = df.columns.str.strip().str.upper().str.replace(r'\s+', '_', regex=True)

# Drop fully duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Duplicate rows removed   : {before - len(df):,}")

# Drop rows missing both location AND borough (not usable for geo work)
before = len(df)
df = df.dropna(subset=['LATITUDE', 'LONGITUDE', 'BOROUGH'], how='all')
print(f"Rows dropped (no location or borough): {before - len(df):,}")

# Parse CRASH DATE and extract all time features together
df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], errors='coerce')
df['HOUR']        = pd.to_datetime(df['CRASH_TIME'], format='%H:%M', errors='coerce').dt.hour
df['DAY_OF_WEEK'] = df['CRASH_DATE'].dt.dayofweek        # numeric — needed for DAY_TYPE
df['DAY_TYPE']    = df['DAY_OF_WEEK'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
df['DAY_OF_WEEK'] = df['CRASH_DATE'].dt.day_name()       # now safe to overwrite with names
df['MONTH']       = df['CRASH_DATE'].dt.month
df['YEAR']        = df['CRASH_DATE'].dt.year

unparseable = df['CRASH_DATE'].isna().sum()
print(f"Unparseable dates        : {unparseable:,}")

# Fix ZIP CODE — should always be a string, never a number
df['ZIP_CODE'] = df['ZIP_CODE'].astype(str).str.zfill(5).str.strip()
df['ZIP_CODE'] = df['ZIP_CODE'].replace({'nan': np.nan, '00000': np.nan})

# Standardize BOROUGH — title case, unknown → NaN
df['BOROUGH'] = df['BOROUGH'].str.strip().str.title()
valid_boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
df.loc[~df['BOROUGH'].isin(valid_boroughs), 'BOROUGH'] = np.nan

# Standardize contributing factors — blank/unspecified → NaN
unspecified = ['Unspecified', '1', '', 'nan']
for col in ['CONTRIBUTING_FACTOR_VEHICLE_1', 'CONTRIBUTING_FACTOR_VEHICLE_2']:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title()
        df[col] = df[col].replace(unspecified, np.nan)

# Standardize vehicle type codes — consolidate common variants
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

if 'VEHICLE_TYPE_CODE_1' in df.columns:
    df['VEHICLE_TYPE_CODE_1'] = (
        df['VEHICLE_TYPE_CODE_1']
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

df['SEVERITY'] = df.apply(assign_severity, axis=1)
severity_labels = {0: 'Property Damage', 1: 'Injury', 2: 'Fatal'}
df['SEVERITY_LABEL'] = df['SEVERITY'].map(severity_labels)

# Summary after cleaning
print(f"\nRows remaining after cleaning: {len(df):,}")
print(f"\nSeverity Distribution:")
print(df['SEVERITY_LABEL'].value_counts().to_string())
print(f"\nBorough Distribution (after cleaning):")
print(df['BOROUGH'].value_counts(dropna=False).to_string())
print(f"\nYear Range: {df['YEAR'].min()} – {df['YEAR'].max()}")
print("\n[INFO] Basic cleaning complete.\n")


#--------------------------------------------#
# PART 3: Visualization — Crashes by Hour
#--------------------------------------------#

# Aggregate: crash count by HOUR and DAY_TYPE
hourly = (
    df.dropna(subset=['HOUR'])
    .groupby(['HOUR', 'DAY_TYPE'])
    .size()
    .reset_index(name='CRASH_COUNT')
)

weekday = hourly[hourly['DAY_TYPE'] == 'Weekday'].set_index('HOUR')['CRASH_COUNT']
weekend = hourly[hourly['DAY_TYPE'] == 'Weekend'].set_index('HOUR')['CRASH_COUNT']

hours = np.arange(24)
bar_width = 0.4

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

ax.bar(hours - bar_width / 2, weekday.reindex(hours, fill_value=0),
       width=bar_width, label='Weekday', color='#2196F3', alpha=0.85)
ax.bar(hours + bar_width / 2, weekend.reindex(hours, fill_value=0),
       width=bar_width, label='Weekend', color='#FF7043', alpha=0.85)

# Shade rush hour bands
ax.axvspan(7 - 0.5, 9 + 0.5, alpha=0.08, color='gold', label='Rush Hours')
ax.axvspan(16 - 0.5, 18 + 0.5, alpha=0.08, color='gold')

# Labels & formatting
ax.set_xlabel('Hour of Day (0 = Midnight)', fontsize=12, labelpad=10)
ax.set_ylabel('Total Crashes', fontsize=12, labelpad=10)
ax.set_title('NYC Motor Vehicle Crashes by Hour of Day\nWeekday vs. Weekend',
             fontsize=15, fontweight='bold', pad=15)
ax.set_xticks(hours)
ax.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_xlim(-0.7, 23.7)
ax.annotate('Shaded bands = morning (7–9 AM) and evening (4–6 PM) rush hours',
            xy=(0.01, 0.97), xycoords='axes fraction',
            fontsize=8, color='gray', va='top')

plt.tight_layout()
plt.savefig('crashes_by_hour.png', dpi=150, bbox_inches='tight')
print("[INFO] Chart saved to 'crashes_by_hour.png'")

plt.show()