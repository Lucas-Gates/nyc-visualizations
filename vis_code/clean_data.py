import pandas as pd
import numpy as np
from vis_code.extra_funcs import typewrite

# ── Constants ────────────────────────────────────────────────────────────────

DATA_PATH = r"Data\Motor_Vehicle_Collisions_-_Crashes_20260421.csv"

VALID_BOROUGHS = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]

UNSPECIFIED = ["Unspecified", "1", "", "nan"]

VEHICLE_MAP = {
    "Sedan"      : ["Sedan", "4 Dr Sedan", "2 Dr Sedan", "Passenger Vehicle"],
    "SUV"        : ["Station Wagon/Sport Utility Vehicle", "Suv", "Standing S"],
    "Taxi"       : ["Taxi", "Taxi Cab"],
    "Bus"        : ["Bus", "Omnibus", "School Bus"],
    "Truck"      : ["Truck", "Pick-Up Truck", "Box Truck", "Flat Bed", "Dump"],
    "Motorcycle" : ["Motorcycle", "Motorbike"],
    "Bicycle"    : ["Bike", "Bicycle", "E-Bike"],
}

SEVERITY_LABELS = {0: "Property Damage", 1: "Injury", 2: "Fatal"}

MAX_CASUALTIES = 20    # pedestrians and cyclists
MAX_INJURIES   = 100   # persons and motorists

CASUALTY_THRESHOLDS = {
    "NUMBER_OF_PERSONS_INJURED"      : MAX_INJURIES,
    "NUMBER_OF_PERSONS_KILLED"       : MAX_CASUALTIES,
    "NUMBER_OF_PEDESTRIANS_INJURED"  : MAX_CASUALTIES,
    "NUMBER_OF_PEDESTRIANS_KILLED"   : MAX_CASUALTIES,
    "NUMBER_OF_CYCLIST_INJURED"      : MAX_CASUALTIES,
    "NUMBER_OF_CYCLIST_KILLED"       : MAX_CASUALTIES,
    "NUMBER_OF_MOTORIST_INJURED"     : MAX_INJURIES,
    "NUMBER_OF_MOTORIST_KILLED"      : MAX_CASUALTIES,
}


# ── Misc. Functions ──────────────────────────────────────────────────────────────────

def _assign_severity(row):
    """Returns a severity score: 0 = property damage, 1 = injury, 2 = fatal."""
    if row.get("NUMBER_OF_PERSONS_KILLED", 0) > 0:
        return 2
    elif row.get("NUMBER_OF_PERSONS_INJURED", 0) > 0:
        return 1
    return 0


# ── Main Function ────────────────────────────────────────────────────────────

def load_and_clean_data():
    """
    Loads the NYC Motor Vehicle Collisions CSV and performs all cleaning steps.
    Returns a cleaned DataFrame ready for analysis and visualization.

    Cleaning steps:
        1.  Load CSV
        2.  Standardize column names
        3.  Drop duplicates and unlocatable rows
        4.  Parse crash date/time and extract time features
        5.  Clean ZIP_CODE and BOROUGH
        6.  Standardize contributing factors
        7.  Consolidate vehicle type labels
        8.  Assign severity scores and labels
        9.  Remove impossible casualty values
    """

    # ── 1. Load ──────────────────────────────────────────────────────
    typewrite("Loading data")
    df_clean = pd.read_csv(DATA_PATH, low_memory=False)

    print()
    print("══════════════════════════════════════")
    print("►  Cleaning Data  —  est. 3 minutes  ◄")
    print("══════════════════════════════════════\n")

    # ── 2. Standardize Column Names ──────────────────────────────────
    typewrite("Formatting headers")
    df_clean.columns = (
        df_clean.columns
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "_", regex=True)
    )

    # ── 3. Drop Duplicates & Unlocatable Rows ────────────────────────
    typewrite("Dropping duplicates and nulls")
    df_clean = (
        df_clean
        .drop_duplicates()
        .dropna(subset=["LATITUDE", "LONGITUDE", "BOROUGH"], how="all")
    )

    # ── 4. Parse Dates & Extract Time Features ───────────────────────
    typewrite("Parsing dates and times")
    df_clean["CRASH_DATE"] = pd.to_datetime(df_clean["CRASH_DATE"], errors="coerce")
    df_clean["HOUR"]       = pd.to_datetime(df_clean["CRASH_TIME"], format="%H:%M", errors="coerce").dt.hour

    typewrite("Extracting date components")
    df_clean["DAY_OF_WEEK"] = df_clean["CRASH_DATE"].dt.dayofweek         # Numeric — needed for DAY_TYPE
    df_clean["DAY_TYPE"]    = df_clean["DAY_OF_WEEK"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")
    df_clean["DAY_OF_WEEK"] = df_clean["CRASH_DATE"].dt.day_name()        # Now safe to overwrite with names
    df_clean["MONTH"]       = df_clean["CRASH_DATE"].dt.month
    df_clean["YEAR"]        = df_clean["CRASH_DATE"].dt.year

    # ── 5. Clean ZIP_CODE & BOROUGH ──────────────────────────────────
    typewrite("Cleaning ZIP_CODE and BOROUGH")
    df_clean["ZIP_CODE"] = (
        df_clean["ZIP_CODE"]
        .astype(str).str.zfill(5).str.strip()
        .replace({"nan": np.nan, "00000": np.nan})
    )

    df_clean["BOROUGH"] = df_clean["BOROUGH"].str.strip().str.title()
    df_clean.loc[~df_clean["BOROUGH"].isin(VALID_BOROUGHS), "BOROUGH"] = np.nan

    # ── 6. Standardize Contributing Factors ──────────────────────────
    typewrite("Cleaning contributing factors")
    for col in ["CONTRIBUTING_FACTOR_VEHICLE_1", "CONTRIBUTING_FACTOR_VEHICLE_2"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip().str.title().replace(UNSPECIFIED, np.nan)

    # ── 7. Consolidate Vehicle Type Labels ───────────────────────────
    # Invert VEHICLE_MAP so each variant maps to its canonical label
    typewrite("Consolidating vehicle type labels")
    lookup = {v.lower(): k for k, variants in VEHICLE_MAP.items() for v in variants}

    if "VEHICLE_TYPE_CODE_1" in df_clean.columns:
        df_clean["VEHICLE_TYPE_CODE_1"] = (
            df_clean["VEHICLE_TYPE_CODE_1"]
            .str.strip().str.title()
            .map(lambda x: lookup.get(str(x).lower(), x) if pd.notna(x) else np.nan)
        )

    # ── 8. Assign Severity Scores & Labels ───────────────────────────
    typewrite("Assigning severity labels")
    df_clean["SEVERITY"]       = df_clean.apply(_assign_severity, axis=1)
    df_clean["SEVERITY_LABEL"] = df_clean["SEVERITY"].map(SEVERITY_LABELS)

    # ── 9. Remove Impossible Casualty Values ─────────────────────────
    # Injuries capped at 100 for persons/motorists, 20 for pedestrians/cyclists
    # Values exceeding these thresholds are likely data entry errors
    typewrite("Validating casualty & injury counts")
    for col, threshold in CASUALTY_THRESHOLDS.items():
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
            df_clean.loc[df_clean[col] > threshold, col] = np.nan

    print(f"\nRows remaining after cleaning: {len(df_clean):,}")
    return df_clean