import plotly.express as px

def parallel(data):
    data_parallel = data.copy()

    # Filter to 2025 only
    data_parallel = data_parallel[data_parallel['YEAR'] == 2025]

    # Aggregate: crashes and average severity by vehicle type
    vehicle_agg = (
        data_parallel.dropna(subset=['VEHICLE_TYPE_CODE_1'])
        .groupby('VEHICLE_TYPE_CODE_1')
        .agg(
            CRASH_COUNT=('COLLISION_ID', 'size'),
            AVG_SEVERITY=('SEVERITY', 'mean')
        )
        .reset_index()
    )

    # Keep only vehicle types with at least 100 crashes to reduce clutter
    vehicle_agg = vehicle_agg[vehicle_agg['CRASH_COUNT'] >= 100].reset_index(drop=True)

    # Encode vehicle type as numeric for parallel coordinates
    vehicle_agg['VEHICLE_TYPE_NUM'] = range(len(vehicle_agg))

    fig = px.parallel_coordinates(
        vehicle_agg,
        dimensions=['VEHICLE_TYPE_NUM', 'CRASH_COUNT', 'AVG_SEVERITY'],
        color='AVG_SEVERITY',
        color_continuous_scale=[[0, 'teal'], [1, 'red']],
        labels={
            'VEHICLE_TYPE_NUM' : 'Vehicle Type',
            'CRASH_COUNT'      : 'Number of Crashes',
            'AVG_SEVERITY'     : 'Avg Severity'
        },

        title='NYC Crashes (2025) - Vehicle Type vs. Crash Count vs. Severity'
    )

    # Map numeric ticks back to vehicle names
    vehicle_names = vehicle_agg['VEHICLE_TYPE_CODE_1'].tolist()
    fig.data[0].dimensions[0].tickvals = vehicle_agg['VEHICLE_TYPE_NUM'].tolist()
    fig.data[0].dimensions[0].ticktext = vehicle_names

    fig.update_layout(
        coloraxis_colorbar=dict(
        title=dict(text='Avg Severity', font=dict(color='white')),
        tickfont=dict(color='white')),
        font=dict(size=11, color='white'),
        title_font=dict(size=14, color='white'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        width=1400,
        height=600,
        margin=dict(l=150, r=150, t=80, b=80))

    fig.write_html('figures/fig5_parallel_coords_vehicle.html')
    print("Figure saved as 'figures/fig5_parallel_coords_vehicle.html'\n")

    fig.show()