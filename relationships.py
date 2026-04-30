import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import plotly.express as px

data = pd.read_csv("./data/Motor_Vehicle_Collisions_-_Crashes_20260421.csv",low_memory=False)

###data = data[::5]


data = data[data['LATITUDE'].notna() & data['LONGITUDE'].notna()]
data = data.drop(columns = ['ZIP CODE'])
data = data[data['NUMBER OF PERSONS INJURED'].notna() & data['NUMBER OF PERSONS KILLED'].notna()]

data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])





data['YEAR'] = data['CRASH DATE'].dt.year

data = data[data['YEAR'] != 2026]
years = data.groupby('YEAR').agg(
    CRASH_COUNT=('COLLISION_ID', 'size'),
    TOTAL_INJURED=('NUMBER OF PERSONS INJURED', 'sum'),
    AVG_INJURED=('NUMBER OF PERSONS INJURED', 'mean')
).reset_index()

min_s, max_s = 10, 60  # control your min/max dot size

years['SIZES'] = (years['AVG_INJURED'] - years['AVG_INJURED'].min()) / \
        (years['AVG_INJURED'].max() - years['AVG_INJURED'].min()) \
        * (max_s - min_s) + min_s




fig = px.scatter(years, x='YEAR', y='CRASH_COUNT', size='AVG_INJURED', 
                 hover_data=['YEAR', 'CRASH_COUNT', 'AVG_INJURED'],
                 labels ={'YEAR': 'Year', 'CRASH_COUNT': 'Number of Crashes', 'AVG_INJURED': 'Average Injuries per Incident'},title = 'NYC\'s Decline in Crashes, Increase in Danger ',  size_max= 120)
fig.write_html("crashDanger.html")

fig.show()


