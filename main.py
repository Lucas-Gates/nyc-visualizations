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

df = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes_20260421.csv')

# First 5 rows
print("First 5 Rows: \n")
print(df.head(), "\n")

# Number of rows & columns
print(f"Total Number of Rows: {df.shape[0]}\nTotal Number of Columns: {df.shape[1]} \n")

# Column names
print("Column Names: ", df.columns, "\n")

# Data types
print("Data Types:\n", df.dtypes.to_string(), "\n")