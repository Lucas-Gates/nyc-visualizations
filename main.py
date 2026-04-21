import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


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
 
# Parse CRASH DATE as a proper datetime
df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], errors='coerce')
unparseable = df['CRASH_DATE'].isna().sum()
print(f"Unparseable dates        : {unparseable:,}")
 
# Extract useful time features
df['HOUR']        = pd.to_datetime(df['CRASH_TIME'], format='%H:%M', errors='coerce').dt.hour
df['DAY_OF_WEEK'] = df['CRASH_DATE'].dt.day_name()
df['MONTH']       = df['CRASH_DATE'].dt.month
df['YEAR']        = df['CRASH_DATE'].dt.year
 
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
    'Sedan'             : ['Sedan', '4 Dr Sedan', '2 Dr Sedan', 'Passenger Vehicle'],
    'SUV'               : ['Station Wagon/Sport Utility Vehicle', 'Suv'],
    'Taxi'              : ['Taxi', 'Taxi Cab'],
    'Bus'               : ['Bus', 'Omnibus', 'School Bus'],
    'Truck'             : ['Truck', 'Pick-Up Truck', 'Box Truck', 'Flat Bed'],
    'Motorcycle'        : ['Motorcycle', 'Motorbike'],
    'Bicycle'           : ['Bike', 'Bicycle', 'E-Bike'],
}
# Invert the map: variant → canonical label
lookup = {v.lower(): k for k, variants in vehicle_map.items() for v in variants}
 
if 'VEHICLE_TYPE_CODE_1' in df.columns:
    df['VEHICLE_TYPE_CODE_1'] = (
        df['VEHICLE_TYPE_CODE_1']
        .str.strip().str.title()
        .map(lambda x: lookup.get(str(x).lower(), x) if pd.notna(x) else np.nan)
    )
 
# Create SEVERITY column
#    0 = property damage only, 1 = injury, 2 = fatality
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