import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import plotly.express as px

def relPlot(data):

    data = data[data['YEAR'] != 2026]
    years = data.groupby('YEAR').agg(
        CRASH_COUNT=('COLLISION_ID', 'size'),
        TOTAL_INJURED=('NUMBER_OF_PERSONS_INJURED', 'sum'),
        AVG_INJURED=('NUMBER_OF_PERSONS_INJURED', 'mean')
    ).reset_index()



    years['AVG_INJURED'] = round(years['AVG_INJURED'],2)




    fig = px.scatter(years, x='YEAR', y='CRASH_COUNT', size='AVG_INJURED', 
                    hover_data=['YEAR', 'CRASH_COUNT', 'AVG_INJURED'],
                    labels ={'YEAR': 'Year', 'CRASH_COUNT': 'Number of Crashes', 'AVG_INJURED': 'Injuries per Crash'},title = 'NYC\'s Decline in Crashes, Increase in Danger ',  size_max= 120)
    fig.add_annotation(
        x=1.02, y=0.5,
        xref="paper", yref="paper",
        text="<b>Bubble Size</b><br>= Avg Injuries<br>per Incident",
        showarrow=False,
        align="left",
        bordercolor="gray",
        borderwidth=1,
        bgcolor="white",
        font=dict(size=12)
    )

    fig.update_layout(margin=dict(r=150))

    fig.write_html("crashDanger.html")
    return fig


    
