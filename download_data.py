import pandas as pd

#url filtered to 2025
url = "https://data.cityofnewyork.us/resource/h9gi-nx95.csv?$where=crash_date%20between%20'2025-01-01T00:00:00'%20and%20'2025-12-31T23:59:59'&$limit=5000000"

#save location
output_path = "data/new_DATA.csv"

#download
df = pd.read_csv(url, low_memory=False)
df.to_csv(output_path, index=False)
print(f"downloaded dataset to {output_path}")