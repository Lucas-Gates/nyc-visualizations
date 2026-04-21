import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

data = pd.read_csv("./data/Motor_Vehicle_Collisions_-_Crashes_20260421.csv")

print(data.head())
print(f"\nThe data has {len(data)} rows and {len(data.columns)} columns\n")
print("Column Names: ")
for c in data.columns:
    print(f"\t{c}")
print("\n")
print(data.dtypes)
print("\n")


data = data[data['LATITUDE'].notna() & data['LONGITUDE'].notna()]
data = data.drop(columns = ['ZIP CODE'])
data = data[data['NUMBER OF PERSONS INJURED'].notna() & data['NUMBER OF PERSONS KILLED'].notna()]

print("Missing Values:")
print(data.isna().sum())


