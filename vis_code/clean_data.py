import pandas as pd
import numpy as np


def load_and_clean_data():
    df = pd.read_csv(r"Data\Motor_Vehicle_Collisions_-_Crashes_20260421.csv", low_memory=False)

    df_clean = df.copy()

    print("Formatting headers...")
    df_clean.columns = df_clean.columns.str.strip().str.upper().str.replace(r"\s+", "_", regex=True)

    print("Dropping duplicates and nulls...")
    df_clean = df_clean.drop_duplicates()

    df_clean = df_clean.dropna(subset=["LATITUDE", "LONGITUDE", "BOROUGH"], how="all")

    print("Parsing dates and times...")
    df_clean["CRASH_DATE"] = pd.to_datetime(df_clean["CRASH_DATE"], errors="coerce")
    df_clean["HOUR"] = pd.to_datetime(df_clean["CRASH_TIME"], format="%H:%M", errors="coerce").dt.hour

    print("Extracting date components...")
    df_clean["DAY_OF_WEEK"] = df_clean["CRASH_DATE"].dt.dayofweek
    df_clean["DAY_TYPE"] = df_clean["DAY_OF_WEEK"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")
    df_clean["DAY_OF_WEEK"] = df_clean["CRASH_DATE"].dt.day_name()
    df_clean["MONTH"] = df_clean["CRASH_DATE"].dt.month
    df_clean["YEAR"] = df_clean["CRASH_DATE"].dt.year

    print("Cleaning ZIP_CODE and BOROUGH...")
    df_clean["ZIP_CODE"] = df_clean["ZIP_CODE"].astype(str).str.zfill(5).str.strip()
    df_clean["ZIP_CODE"] = df_clean["ZIP_CODE"].replace({"nan": np.nan, "00000": np.nan})

    df_clean["BOROUGH"] = df_clean["BOROUGH"].str.strip().str.title()

    valid_boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
    df_clean.loc[~df_clean["BOROUGH"].isin(valid_boroughs), "BOROUGH"] = np.nan

    unspecified = ["Unspecified", "1", "", "nan"]

    print("Cleaning contributing factors and vehicle types...")
    for col in ["CONTRIBUTING_FACTOR_VEHICLE_1", "CONTRIBUTING_FACTOR_VEHICLE_2"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip().str.title()
            df_clean[col] = df_clean[col].replace(unspecified, np.nan)

    vehicle_map = {
        "Sedan": ["Sedan", "4 Dr Sedan", "2 Dr Sedan", "Passenger Vehicle"],
        "SUV": ["Station Wagon/Sport Utility Vehicle", "Suv"],
        "Taxi": ["Taxi", "Taxi Cab"],
        "Bus": ["Bus", "Omnibus", "School Bus"],
        "Truck": ["Truck", "Pick-Up Truck", "Box Truck", "Flat Bed"],
        "Motorcycle": ["Motorcycle", "Motorbike"],
        "Bicycle": ["Bike", "Bicycle", "E-Bike"],
    }

    lookup = {v.lower(): k for k, values in vehicle_map.items() for v in values}

    if "VEHICLE_TYPE_CODE_1" in df_clean.columns:
        df_clean["VEHICLE_TYPE_CODE_1"] = (
            df_clean["VEHICLE_TYPE_CODE_1"]
            .str.strip()
            .str.title()
            .map(lambda x: lookup.get(str(x).lower(), x) if pd.notna(x) else np.nan)
        )

    print("Assigning severity labels...")
    def assign_severity(row):
        if row.get("NUMBER_OF_PERSONS_KILLED", 0) > 0:
            return 2
        elif row.get("NUMBER_OF_PERSONS_INJURED", 0) > 0:
            return 1
        else:
            return 0

    df_clean["SEVERITY"] = df_clean.apply(assign_severity, axis=1)

    severity_labels = {
        0: "Property Damage",
        1: "Injury",
        2: "Fatal"
    }

    df_clean["SEVERITY_LABEL"] = df_clean["SEVERITY"].map(severity_labels)

    print("Rows remaining after cleaning:", len(df_clean))

    return df_clean